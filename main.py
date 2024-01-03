from collections import namedtuple
from datetime import datetime
from database.db_service import DbManager, DataBaseService
from database.db_service import DbManager
import smtplib, ssl
from os import environ, getenv
import sqlite3


connection = sqlite3.connect('database/sample_books.db') #być może trzeba będzie to zostawić

db = DataBaseService(connection)

# print(db.get_borrowed_books_by_today())
print(db.get_borrowed_books_by_today())



class MailSender():
    @staticmethod
    def send_data(func):
        def wrapper(*args, **kwargs):
            #TODO create funcion that sends email using data from .env, than in different methods, sends emails with specific message
            smtp_server = getenv('SMTP_SERVER')
            port = getenv('PORT')
            sender_email = getenv('EMAIL')
            password = getenv('PASSWORD')

            context = ssl.create_default_context()

            result = func(*args, smtp_server = smtp_server, port = port, sender_email = sender_email, password = password, context = context)

            return result

        return wrapper

    def __init__(self, user: namedtuple):
        self.user = user

    @send_data
    def send_passed_return_date(self, smtp_server, port, sender_email, password, context, receiver_email, msg):
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg=msg)






