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
    account_url = os.getenv("AZFUNC_ACCOUNT_URL")
    account_key = os.getenv("AZFUNC_ACCOUNT_KEY", None)
    logging.info(f"account url: {account_url} \naccount key: {account_key}")
    if not account_url:
        raise ValueError("AZFUNC_ACCOUNT_URL is not set")
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=account_key or DefaultAzureCredential()
    )
