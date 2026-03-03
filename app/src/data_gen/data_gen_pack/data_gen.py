from datetime import date
from typing import List
import random
import uuid

from faker import Faker


def generate_clients(n: int) -> list:
    fake = Faker()

    end_datetime = date(
        year=2010,
        month=1,
        day=1
    )
    clients = [
        {
            "id": uuid.uuid4().hex,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "birth_date": fake.date(end_datetime=end_datetime)
        }
        for i in range(n)
    ]
    return clients

def generate_books(n: int) -> list:
    fake = Faker()

    books = [
        {
            "id": uuid.uuid4().hex,
            "book_name": fake.sentence(),
            "author": fake.name(),
            "price": round(random.random() * 100, 2),
        }
        for i in range(n)
    ]
    return books

def generate_orders(n: int, clients: List[dict], books: List[dict]) -> list:
    fake = Faker()
    client_ids = [client["id"] for client in clients]

    orders = []
    for i in range(n):
        order_items = random.choices(books, k=random.randint(1, 10))
        for order in order_items:
            order["quantity"] = random.randint(1, 5)
        
        orders.append(
            {
                "id": uuid.uuid4().hex,
                "client_id": random.choice(client_ids),
                "order_items": order_items,
                "order_timestamp": str(fake.date_time_this_decade())
            }
        )
    return orders