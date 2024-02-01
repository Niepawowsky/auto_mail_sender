"""
Testing db_service
"""

import sqlite3
import pytest
from freezegun import freeze_time
from database.db_service import DataBaseService



@pytest.fixture
def make_connection():

    """
    The create_connection function creates a connection to the database.
        Args:
            None

    :return: A connection object
    :doc-author: Trelent
    """
    with sqlite3.connect(':memory:') as connection:
        return connection


@freeze_time('2024-01-08 00:00:00')
def test_get_borrowed_books_for_today_reminder_purpose(make_connection):

    """
    The test_get_borrowed_books_for_today_reminder_purpose
    function tests the get_borrowed_books_by_today function.
    It checks if it returns a list of borrowers who borrowed books today.

    :param create_connection: Create a connection to the database
    :param monkeypatch: Mock the current time
    :return: A list of borrowers
    :doc-author: Trelent
    """
    db = DataBaseService(make_connection)
    db.create_database()
    query = 'INSERT INTO borrowed_books VALUES(?,?,?,?,?,?)'
    sample_data = [
        (6, 'John Smith', 'sample@email.com',
         'Lalka', 'Bolesław Prus', '2024-12-27 13:30:30'),
        (7, 'Luiza Acante', 'sample@email.com',
         'Engine Manual for Smartasses', 'Mario Bro', '2023-12-27 13:30:30')
    ]
    for data in sample_data:
        db.execute_query(query, data)

    list_of_borrowers = db.get_borrowed_books_by_today()

    assert len(list_of_borrowers) == 1


@freeze_time('2024-01-08 00:00:00')
def test_get_borrowed_books_for_today_amount_of_records(make_connection):

    """
    The test_get_borrowed_books_for_today_amount_of_records
    function tests the get_borrowed_passed function from DataBaseService class.
    It checks if the amount of records returned by this function is correct.


    :param create_connection: Create a connection to the database
    :return: 1 because the second record has a date in the future
    :doc-author: Trelent
    """
    db = DataBaseService(make_connection)
    db.create_database()
    query = 'INSERT INTO borrowed_books VALUES(?,?,?,?,?,?)'
    sample_data = [
        (6, 'sample@email.com', 'John Smith', 'Lalka',
         'Bolesław Prus', '2024-12-27 13:30:30'),
        (7, 'sample@email.com', 'Luiza Acante', 'Engine Manual for Smartasses',
         'Mario Bro', '2023-12-27 13:30:30')
    ]
    for data in sample_data:
        db.execute_query(query, data)

    list_of_borrowers = db.get_borrowed_passed()
    assert len(list_of_borrowers) == 1
