import os
import logging
import uuid
import json
from datetime import datetime

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from data_gen_pack import generate_clients, generate_books, generate_orders


LANDING_CONTAINER_NAME = "ci-dataproject-landing"
CLIENTS_PATH = "clients"
BOOKS_PATH = "books"
ORDERS_PATH = "orders"


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

    container = blob_service_client.get_container_client(LANDING_CONTAINER_NAME)

    client_blobs = container.list_blob_names(name_starts_with=f"{CLIENTS_PATH}/")
    if not list(client_blobs):
        clients_data = generate_clients(50)
        clients_payload = json.dumps(clients_data).encode("utf-8")
        clients_blob = container.get_blob_client(f"{CLIENTS_PATH}/clients.json")
        clients_blob.upload_blob(clients_payload)
    else:
        clients_blob = container.get_blob_client(f"{CLIENTS_PATH}/clients.json")
        clients_download = clients_blob.download_blob()
        clients_content = clients_download.readall().decode("utf-8")
        clients_data = json.loads(clients_content)
    
    book_blobs = container.list_blob_names(name_starts_with=f"{BOOKS_PATH}/")
    if not list(book_blobs):
        books_data = generate_books(100)
        books_payload = json.dumps(books_data).encode("utf-8")
        books_blob = container.get_blob_client(f"{BOOKS_PATH}/books.json")
        books_blob.upload_blob(books_payload)
    else:
        books_blob = container.get_blob_client(f"{BOOKS_PATH}/books.json")
        books_download = books_blob.download_blob()
        books_content = books_download.readall().decode("utf-8")
        books_data = json.loads(books_content)

    # create orders
    orders = generate_orders(100, clients_data, books_data)
    orders_payload = json.dumps(orders).encode("utf-8")
    orders_file_name = f"{uuid.uuid4().hex}-{datetime.now()}.json"
    orders_blob = container.get_blob_client(f"{ORDERS_PATH}/{orders_file_name}")
    orders_blob.upload_blob(orders_payload)

