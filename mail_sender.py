'''
Module that gathers objects from template_render.py and db_service.py.
Main logic is placed here. Proper message is sent to selected persons from database
'''

import smtplib
import ssl
from os import getenv
from dotenv import load_dotenv
from templates.template_render import EmailTemplates
from database.db_service import DataBaseService


class MailSender():
    '''
    It's a class that creates proper mail message to proper user, that have borrowed a book.
    It collects info from db_service and template_render and combines it togheter
    '''

    @staticmethod
    def send_data(func):

        """
        The send_data function is a decorator that adds the
        following keyword arguments to the function it wraps:
        smtp_server, port, sender_email, password and context.
        These are all required for sending an email using Python's
        built-in smtplib module. The send_data function also loads environment
        variables from a .env file in order to keep
        sensitive information such as passwords out of source code.

        :param func: Pass the function that we want to decorate
        :return: A function
        :doc-author: Trelent
        """
        def wrapper(*args, **kwargs):
            load_dotenv()
            smtp_server = getenv('SMTP_SERVER')
            port = 465  # or int(getenv('PORT'))
            sender_email = getenv('EMAIL')
            password = getenv('PASSWORD')
            context = ssl.create_default_context()

            kwargs.update({
                'smtp_server': smtp_server,
                'port': port,
                'sender_email': sender_email,
                'password': password,
                'context': context

            })
            result = func(*args, **kwargs)
            return result

        return wrapper

    def __init__(self, template: EmailTemplates, connection: DataBaseService):
        self.template = template
        self.connection = connection

    @send_data
    def send_passed_return_date(self, **kwargs):

        """
            The send_passed_return_date function sends an email to the borrower
            of a book that has passed its return date.
            The function takes in the following arguments:
            sender_email - The email address from which the reminder will be sent.
            password - The password for sender_email, used to authenticate with smtp server.
            smtp_server - The SMTP server through which emails are sent
            (e.g., 'smtp-mail.outlook.com').
            port - Port number for SMTP server (e.g., 587).

        :param self: Refer to the instance of the class
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of all the borrowers who have borrowed books that are overdue
        """
        sender = kwargs['sender_email']
        password = kwargs['password']
        borrower_list = self.connection.get_borrowed_passed()

        try:
            #
            with smtplib.SMTP_SSL(host=kwargs['smtp_server'], port=kwargs["port"],
                                  context=kwargs['context']) as server:
                for borrower in borrower_list:
                    name = borrower.name
                    title = borrower.title
                    return_at = borrower.return_at
                    borrower_email = borrower.email
                    subject = "Book return reminder"
                    mail = self.template.send_reminder_overdue(sender, borrower_email,
                                                               name, title, return_at, subject)
                    server.login(sender, password)
                    server.sendmail(from_addr=sender, to_addrs=borrower.email, msg=mail.as_string())

        except Exception as e:
            print(f'Error: {e}')

    def send_incoming_return_date(self, **kwargs):

        """
        The send_incoming_return_date function sends an email
        to the borrower of a book that is due today.
        The function takes in the following arguments:
            sender_email - The email address from which you want to send emails.
                           This should be a gmail account,
                           and it must have &quot;Allow less secure apps&quot;
                           enabled (see https://support.google.com/accounts/answer/6010255?hl=en)

        :param self: Refer to the current instance of the class
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: None
        :doc-author: Trelent
        """
        sender = kwargs['sender_email']
        password = kwargs['password']
        borrower_list = self.connection.get_borrowed_books_by_today()

        try:
            with smtplib.SMTP_SSL(host=kwargs['smtp_server'], port=kwargs["port"],
                                  context=kwargs['context']) as server:
                for borrower in borrower_list:
                    name = borrower.name
                    title = borrower.title
                    return_at = borrower.return_at
                    borrower_email = borrower.email
                    subject = "Book return reminder"
                    mail = self.template.send_reminder_overdue(sender, borrower_email,
                                                               name, title, return_at, subject)
                    server.login(sender, password)
                    server.sendmail(from_addr=sender, to_addrs=borrower.email, msg=mail.as_string())

        except Exception as e:
            print(f'Error: {e}')
