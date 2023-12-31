from collections import namedtuple
from datetime import datetime
from database.db_service import DbManager, DataBaseService
from database.db_service import DbManager
import sqlite3

connection = sqlite3.connect('database/sample_books.db') #być może trzeba będzie to zostawić

db= DataBaseService(connection)

# print(db.get_borrowed_books_by_today())
print(db.get_borrowed_for_remider())

