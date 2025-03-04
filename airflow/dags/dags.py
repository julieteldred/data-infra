import os
import airflow  # noqa

from pathlib import Path
from gusty import create_dag


# DAG Directories =============================================================

# point to your dags directory
dag_parent_dir = Path(os.environ["AIRFLOW_HOME"]) / "dags"

# TODO: catalogs directory is not a dag, which screws up auto loading folders
# assumes any subdirectories in the dags directory are Gusty DAGs (with METADATA.yml)
# (excludes subdirectories like __pycache__)
# dag_directories = []
# for child in dag_parent_dir.iterdir():
#     if child.is_dir() and not str(child).endswith('__'):
#         dag_directories.append(str(child))

dag_directories = [dag_parent_dir / "gtfs_downloader"]


# DAG Generation ==============================================================

for dag_directory in dag_directories:
    dag_id = os.path.basename(dag_directory)
    globals()[dag_id] = create_dag(
        dag_directory,
        tags=["default", "tags"],
        task_group_defaults={"tooltip": "this is a default tooltip"},
        wait_for_defaults={"retries": 10, "check_existence": True},
        latest_only=False,
    )
