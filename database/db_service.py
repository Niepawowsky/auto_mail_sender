import sqlite3
from collections import namedtuple
from datetime import datetime, date


class DbManager:
    """
    Context manager created for creation or wraping database
    """

    def __init__(self, connection) -> None:
        self.connection = connection
        print('init statement')
        self.cursor = None

    def __enter__(self):
        self.cursor = self.connection.cursor()
        print('Enter statement')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit statement')
        if isinstance(exc_val, Exception):
            self.connection.rollback()
            print('isinstance print')
        else:
            self.connection.commit()
            print('commiting query')

        # self.connection.close()
        # print('Connection closed')


class DataBaseService():

    def __init__(self, connection):
        self.connection = connection

    def create_database(self, connection):
        with DbManager(connection) as database:
            database.cursor.execute('''CREATE TABLE IF NOT EXISTS borrowed_books(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    name TEXT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    return_at DATE)'''
                                    )

    def get_borrowed_books_by_today(self):

        """
        The get_borrowed_books_by_today function returns a list of
        namedtuples containing the name, email, title and return_at
        of all books that are overdue. The return_at is converted to a datetime object for easier comparison.

        :param self: Represent the instance of the class
        :return: A list of borrowers
        """
        today = datetime.today()
        borrower = namedtuple('Borrower', 'name email title return_at')
        borrower_list = []
        with DbManager(connection=self.connection) as database:
            database.cursor.execute('''SELECT 
                name, 
                email, 
                title, 
                return_at 
            FROM borrowed_books
            WHERE return_at < ?''', (today,))

            for name, email, title, return_at in database.cursor.fetchall():
                return_date = datetime.strptime(return_at, '%Y-%m-%d %H:%M:%S')
                borrower_list.append(borrower(name, email, title, return_date))

            return borrower_list

    def get_borrowed_history(self):
        """
        The get_borrowed_for_remider function returns a list of
        namedtuples containing the name, email, title and return_at
        for each book that is currently borrowed.
        The function will be used to send reminder emails to users who have overdue books.

        :param self: Represent the instance of the class
        :return: A list of named tuples
        """
        # today = datetime.today()
        borrower = namedtuple('Borrower', 'name email title return_at')
        borrower_list = []
        with DbManager(connection=self.connection) as database:
            database.cursor.execute('''SELECT 
                name, 
                email, 
                title, 
                return_at 
            FROM borrowed_books''')

            for name, email, title, return_at in database.cursor.fetchall():
                return_date = datetime.strptime(return_at, '%Y-%m-%d %H:%M:%S')
                print(return_date)
                borrower_list.append(borrower(name, email, title, return_date))

            return borrower_list
