import subprocess
import time
import json
from pathlib import Path
import logging

import pytest
from azure.storage.blob import BlobServiceClient


@pytest.fixture()
def blob_service_client():
    env_path = Path(__file__).parents[2]
    with open(env_path / "local.settings.json", "r") as local_env:
        local_data = json.loads(local_env.read())
        account_url = local_data["Values"]["AZFUNC_ACCOUNT_URL"]
        account_key = local_data["Values"]["AZFUNC_ACCOUNT_KEY"]
    
    if not account_url:
        raise ValueError("AZFUNC_ACCOUNT_URL is not set")
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=account_key
    )
    return blob_service_client

@pytest.fixture(autouse=True)
def set_local_env(blob_service_client: BlobServiceClient):
    logging.info("Creating container in azurite environment...")
    container = blob_service_client.create_container(name="ci-dataproject", timeout=15)
    yield
    container.delete_container()


def test_function(blob_service_client: BlobServiceClient):
    result = subprocess.Popen(
        ["func", "start"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1 
    )
    
    time.sleep(5)

    result.terminate()

    logging.info(result)

    assert blob_service_client.get_container_client("ci-dataproject").exists()


