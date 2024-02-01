'''
Main module to start app
'''
import sqlite3

from mail_sender import MailSender
from database.db_service import DataBaseService
from templates.template_render import EmailTemplates

connection = sqlite3.connect('database/sample_books.db')

data = DataBaseService(connection)
templates = EmailTemplates()

choice = input('What would you like to do?\n'
               'Press button:\n'
               '1 - Send overdue notifications\n'
               '2 - Send nearby notifications\n'
               '3 - Exit')

if choice == '1':
    email = MailSender(templates, data)
    email.send_passed_return_date()
elif choice == '2':
    email = MailSender(templates, data)
    email.send_incoming_return_date()
else:
    print('Wrong button\nStart again!')
