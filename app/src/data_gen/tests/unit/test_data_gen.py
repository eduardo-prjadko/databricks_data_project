import logging

from ...data_gen_pack import generate_clients, generate_books, generate_orders


def test_generate_clients():
    n = 10
    result = generate_clients(n)

    logging.info(result[:2])

    assert len(result) == n


def test_generate_books():
    n = 10
    result = generate_books(n)

    logging.info(result[:2])

    assert len(result) == n

def test_generate_orders():
    n = 10
    clients = generate_clients(n)
    books = generate_books(n)

    result = generate_orders(n, clients, books)

    logging.info(result[:1])

    assert len(result) == n
