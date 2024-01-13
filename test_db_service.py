import pytest

from database.db_service import DataBaseService
import sqlite3
import datetime
import unittest
from freezegun import freeze_time


@pytest.fixture
def create_connection():
    with sqlite3.connect(':memory:') as connection:
        return connection


@freeze_time('2024-01-08 00:00:00')
def test_get_borrowed_books_for_today_reminder_purpose(create_connection, monkeypatch):
    db = DataBaseService(create_connection)
    db.create_database()
    query = 'INSERT INTO borrowed_books VALUES(?,?,?,?,?,?)'
    sample_data = [
        (6, 'sample@email.com', 'John Smith', 'Lalka', 'Bolesław Prus', '2024-12-27 13:30:30'),
        (7, 'sample@email.com', 'Luiza Acante', 'Engine Manual for Smartasses', 'Mario Bro', '2023-12-27 13:30:30')
    ]
    for data in sample_data:
        db._execute_query(query, data)

    list_of_borrowers = db.get_borrowed_books_by_today()

    assert len(list_of_borrowers) == 1


@freeze_time('2024-01-08 00:00:00')
def test_get_borrowed_books_for_today_amount_of_records(create_connection):
    db = DataBaseService(create_connection)
    db.create_database()
    query = 'INSERT INTO borrowed_books VALUES(?,?,?,?,?,?)'
    sample_data = [
        (6, 'sample@email.com', 'John Smith', 'Lalka', 'Bolesław Prus', '2024-12-27 13:30:30'),
        (7, 'sample@email.com', 'Luiza Acante', 'Engine Manual for Smartasses', 'Mario Bro', '2023-12-27 13:30:30')
    ]
    for data in sample_data:
        db._execute_query(query, data)

    list_of_borrowers = db.get_borrowed_history()
    assert len(list_of_borrowers) == 2
