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


    def create_connection(self):
        pass
    def create_database(self):
        with DbManager(self.connection) as database:
            database.cursor.execute('''CREATE TABLE IF NOT EXISTS borrowed_books(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    name TEXT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    return_at DATE)'''
                                    )
    def _execute_query(self, query, params):

        with DbManager(connection=self.connection) as database:
            cursor = database.cursor
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

        return cursor.fetchall()

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
        query = '''SELECT 
                name, 
                email, 
                title, 
                return_at 
            FROM borrowed_books
            WHERE return_at > ?'''

        result = self._execute_query(query, (today,))

        for name, email, title, return_at in result:
            return_date = datetime.strptime(return_at, '%Y-%m-%d %H:%M:%S')
            return_date.strftime('%Y-%m-%d')
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
        query = '''SELECT 
                name, 
                email, 
                title, 
                return_at 
            FROM borrowed_books'''

        result = self._execute_query(query, None)

        for name, email, title, return_at in result:
            return_date = datetime.strptime(return_at, '%Y-%m-%d %H:%M:%S')
            return_date.strftime('%Y-%m-%d')
            borrower_list.append(borrower(name, email, title, return_date))

        return borrower_list


    def add_record(self):
        pass

