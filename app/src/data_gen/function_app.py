import os
import logging
import uuid

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()


@app.timer_trigger(schedule="*/5 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def data_generator(myTimer: func.TimerRequest) -> None:
    
    logging.info("starting data generator...")

    env = os.getenv("ENVIRONMENT")
    logging.info(f"environment: {env}")
    if env == "local":
        account_url = os.getenv("AZFUNC_ACCOUNT_URL")
        account_key = os.getenv("AZFUNC_ACCOUNT_KEY")
        logging.info(f"account url: {account_url} \naccount key: {account_key}")
        if not account_url:
            raise ValueError("AZFUNC_ACCOUNT_URL is not set")
        blob_service_client = BlobServiceClient(
            account_url=account_url,
            credential=account_key
        )
    else:
        account_url = os.getenv("AZFUNC_ACCOUNT_URL")
        default_credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=account_url,
            credential=default_credential,
        )

    logging.info("creating a container...")
    container_name = f"data-{uuid.uuid4().hex[:20]}"
    try:
        container = blob_service_client.create_container(name=container_name, timeout=15)
        logging.info("listing containers...")
        logging.info("created container: %s", container.container_name)
    except Exception:
        logging.exception("failed to create container: %s", container_name)
        raise