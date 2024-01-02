import pytest

from database.db_service import DbManager, DataBaseService
import sqlite3


@pytest.fixture
def create_database():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE borrowed_books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                name TEXT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                return_at DATE)'''
                )

    sample_data = [
        (6, 'sample@email.com', 'John Smith', 'Lalka', 'Bolesław Prus', '2024-12-27 13:30:30'),
        (7, 'sample@email.com', 'Luiza Acante', 'Engine Manual for Smartasses', 'Mario Bro', '2023-12-27 13:30:30')
        ]
    cursor.executemany('INSERT INTO borrowed_books VALUES(?,?,?,?,?,?)', sample_data)
    return cursor


def test_get_borrowed_books_for_today_reminder_purpose(create_database):
    db = DataBaseService
    cursor = create_database
    list_of_borrowers = db.get_borrowed_books_by_today(cursor)
    assert len(list_of_borrowers) == 1

def test_get_borrowed_books_for_today_amount_of_records(create_database):
    db = DataBaseService
    cursor = create_database
    list_of_borrowers = db.get_borrowed_history(cursor)
    assert len(list_of_borrowers) == 2

