import io
import logging
import os
import shutil
import zipfile
from pymongo.database import Database
from dpt.deployment.common import coll_prefix
from dpt.mongo.files import read_file_data

_logger = logging.getLogger(__name__)


def deploy_project(
    workspace_name: str, db: Database, project_name: str, folder_path: str
):
    _logger.info(f"Deploy project: start")
    _logger.info(f"- project_name: {project_name}")
    data = download_project(workspace_name, db, project_name)
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    with zipfile.ZipFile(data, "r") as zip_ref:
        zip_ref.extractall(folder_path)
    _logger.info(f"Deploy project: success")
    _logger.info(f"- folder_path: {folder_path}")


def download_project(workspace_name: str, db: Database, project_name: str):
    _logger.info(f"Download project: start")
    _logger.info(f"- project_name: {project_name}")
    collection = db[f"{coll_prefix}project"]
    info = collection.find_one({"workspace": workspace_name, "name": project_name})
    if info == None:
        raise Exception(f"Project '{project_name}' is not found in database {db.name}")
    data = io.BytesIO(read_file_data(info["file_id"], db))
    _logger.info(f"Download project: success")
    _logger.info(f"- folder_path: {project_name}")
    return data
