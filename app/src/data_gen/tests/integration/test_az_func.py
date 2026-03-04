import subprocess
import time
import json
from pathlib import Path
import logging
import os

import pytest
from azure.storage.blob import BlobServiceClient


@pytest.fixture()
def set_environ():
    os.environ["CONTAINER_NAME"] = "ci-dataproject"

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
def set_local_env(blob_service_client: BlobServiceClient, set_environ):
    contanier_name = os.environ["CONTAINER_NAME"]
    logging.info(f"Checking container {contanier_name}")
    container = blob_service_client.get_container_client(contanier_name)
    if not container.exists():
        logging.info("Creating container in azurite environment...")
        container = blob_service_client.create_container(name=contanier_name, timeout=15)
    else:
        logging.info("Container already exists. Proceding with tests...")
    yield


def test_function(blob_service_client: BlobServiceClient, set_environ):
    container_name = os.environ["CONTAINER_NAME"]
    
    result = subprocess.Popen(
        ["func", "start"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1 
    )
    
    time.sleep(10)

    result.terminate()

    logging.info(result)

    container = blob_service_client.get_container_client(container_name)
    clients_blob = container.get_blob_client("clients/clients.json")

    assert clients_blob.exists()

    books_blob = container.get_blob_client("books/books.json")

    assert books_blob.exists()

    order_blobs = container.list_blob_names(name_starts_with="orders/")

    assert list(order_blobs)
