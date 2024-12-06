import os
import time
import traceback
from pathlib import Path

import gradio as gr
import pandas as pd
import psycopg
import psycopg.crdb
from huggingface_hub import snapshot_download
from sc3020.database.visualizer import Visualizer
from sc3020.whatif import prepare_join_command, prepare_scan_command
from tqdm import tqdm

from ..whatif import (
    JOIN_REGISTRY,
    SCAN_REGISTRY,
    format_set_str,
    prepare_join_command,
    prepare_scan_command,
)
from .ExecutionTree import (
    ExecutionTree,
    ExecutionTreeNode,
    parse_query_explanation_to_tree,
)

PATH_FILE = os.path.dirname(os.path.abspath(__file__))
SETUP_SQL = Path(PATH_FILE) / "setup.sql"
DEFAULT_CACHE_DIR = Path(PATH_FILE).parent / "assets" / "cache"


class TPCHDataset(object):
    def __init__(
        self,
        hf_path: str = "pufanyi/TPC-H",
        max_output_rows: int = 100,
    ):
        super().__init__()
        self.hf_path = hf_path
        self.host_status = False
        self.max_output_rows = max_output_rows
        self.visualizer = Visualizer()

    @property
    def data_path(self):
        # Will fetch the dataset if does not have it
        if not hasattr(self, "_data_path"):
            self._data_path = (
                Path(
                    snapshot_download(
                        repo_id=self.hf_path,
                        allow_patterns="*.tbl",
                        repo_type="dataset",
                    )
                )
                / "raw_data"
            )
        return self._data_path

    @property
    def subsets(self):
        return [x.stem for x in self.data_path.glob("*.tbl")]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.host_status:
            self.conn.close()
            self.host_status = False
        return self

    def host(
        self,
        *,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "tpch",
        user: str = "postgres",
        password,
    ):
        self._db_info = dict(
            host=host, port=port, dbname=dbname, user=user, password=password
        )

        if self.host_status:
            self.close()

        # Connect to the database
        self.conn = psycopg.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cursor = self.conn.cursor()
        self.host_status = True

        return self

    @property
    def db_info(self):
        if not hasattr(self, "_db_info"):
            raise ValueError("Please connect to database first")
        return self._db_info

    def setup(self, **kwargs):
        if not self.host_status:
            if not hasattr(self, "_db_info"):
                self._db_info = {}
            self.db_info.update(kwargs)
            self.host(**self.db_info)
            print("Connected to database")

        for subset in self.subsets:
            self.cursor.execute(f"DROP TABLE IF EXISTS {subset};")

        with open(SETUP_SQL, "r") as f:
            setup_sql = f.read()
        self.cursor.execute(setup_sql)

        for subset in tqdm(self.subsets, desc="Inserting subsets"):
            dataset_path = (self.data_path / f"{subset}.tbl").resolve()
            print(f"Inserting {subset} from {dataset_path}")
            self.cursor.execute(
                f"COPY {subset} FROM '{dataset_path}' DELIMITER '|' CSV;"
            )

        self.conn.commit()

    def explain(self, query: str):
        if not query:
            return None, None, None, None
        try:
            # Execute the Explain command
            self.cursor.execute(f"EXPLAIN {query}")
            explain = self.cursor.fetchall()
            # Parse the explain result into a tree
            tree = parse_query_explanation_to_tree(explain)
            # Traverse the tree to get all the node
            traverse_node = tree.traversal()
            # Get the total cost
            total_cost, startup_cost = tree.get_cost()
            explain_list = []
            # Generate the natural language explanation
            for idx, node in enumerate(traverse_node, 1):
                explain_list.append(f"**Step {idx}**: {node.natural_language()}")
            explain_str = "\n\n".join(explain_list)
            # Visualize the image
            fig = self.visualizer.visualize(tree)
            return explain_str, total_cost, startup_cost, fig
        except Exception as e:
            self.host(**self.db_info)
            return (f"Wrong execution: {str(e)}", 0, 0, None)

    def execute(self, query: str):
        try:
            # Execute the query
            self.cursor.execute(query)
            headers = [desc[0] for desc in self.cursor.description]

            # Execute query and time it
            start_time = time.time()
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            end_time = time.time()
            execution_time = end_time - start_time

            # Convert the result into a DataFrame
            df = pd.DataFrame(results, columns=headers)

            if len(df) > self.max_output_rows:
                messages = {
                    "status": "Success",
                    "message": f"Returned {len(df)} rows, only showing first {self.max_output_rows}",
                    "execution_time": f"{execution_time:.3f} seconds",
                }
                df = df.head(self.max_output_rows)
            else:
                messages = {
                    "status": "Success",
                    "message": f"Returned {len(df)} rows",
                    "execution_time": f"{execution_time:.3f} seconds",
                }
            return df, messages
        except Exception as e:
            self.host(**self.db_info)
            return (
                pd.DataFrame(),
                {"status": "Error", "message": str(traceback.format_exc())},
                "Wrong execution",
            )

    def set_query_config(self, query_config: str):
        # Input will be sth like set xxx=on; set yyy=off;
        try:
            self.cursor.execute(query_config)
        except Exception as e:
            self.host(**self.db_info)
            return {"status": "Error", "message": str(traceback.format_exc())}

    def explain_with_what_if(self, query_input: str, scan_type: str, join_type: str):
        if scan_type == "Default":
            # If the scan type is default, we will set all the scan to on
            scan_command = ""
            for scan in SCAN_REGISTRY:
                scan_command += format_set_str(SCAN_REGISTRY[scan], "on")
            self.set_query_config(scan_command)
        else:
            # else, we set only the scan type to on
            scan_command = prepare_scan_command(scan_type)
            self.set_query_config(scan_command)

        # Same logic here for the join type
        if join_type == "Default":
            join_command = ""
            for join in JOIN_REGISTRY:
                join_command += format_set_str(JOIN_REGISTRY[join], "on")
            self.set_query_config(join_command)
        else:
            join_command = prepare_join_command(join_type)
            self.set_query_config(join_command)

        return self.explain(query_input)


if __name__ == "__main__":
    tpch = TPCHDataset()
    password = os.getenv("POSTGRES_PASSWORD")
    with tpch.host(
        host="localhost",
        port=5432,
        dbname="tpch",
        user="postgres",
        password=password,
    ):
        tpch.setup()
