import sqlite3

from mail_sender import MailSender
from database.db_service import DbManager, DataBaseService
from templates.template_render import EmailTemplates

connection = sqlite3.connect('database/sample_books.db')

data = DataBaseService(connection)
templates = EmailTemplates()
borrowers_list = data.get_borrowed_books_by_today()
print(borrowers_list)

email = MailSender(borrowers_list, templates)
email.send_passed_return_date()

