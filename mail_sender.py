import datetime
import smtplib, ssl
from dotenv import load_dotenv
from os import environ, getenv
from string import Template

from templates.template_render import EmailTemplates


class MailSender():
    @staticmethod
    # def send_data(func):
    #     def wrapper(*args, **kwargs):
    #         smtp_server = getenv('SMTP_SERVER')
    #         port = 465#('PORT')
    #         sender_email = getenv('EMAIL')
    #         password = getenv('PASSWORD')
    #
    #         context = ssl.create_default_context()
    #
    #         result = func(*args,
    #                       smtp_server=smtp_server,
    #                       port=port,
    #                       sender_email=sender_email,
    #                       password=password,
    #                       context=context
    #                       )
    #
    #         return result
    #
    #     return wrapper

    @staticmethod
    def send_data(func):
        def wrapper(*args, **kwargs):
            load_dotenv()
            smtp_server = getenv('SMTP_SERVER')
            port = 465  # or int(getenv('PORT'))
            sender_email = getenv('EMAIL')
            password = getenv('PASSWORD')

            context = ssl.create_default_context()

            # # If the wrapped function already has these arguments, use them
            # if 'smtp_server' in kwargs:
            #     smtp_server = kwargs['smtp_server']
            # if 'port' in kwargs:
            #     port = kwargs['port']
            # if 'sender_email' in kwargs:
            #     sender_email = kwargs['sender_email']
            # if 'password' in kwargs:
            #     password = kwargs['password']
            # if 'context' in kwargs:
            #     context = kwargs['context']

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

    def __init__(self, borrowers: list, template: EmailTemplates):
        self.borrowers = borrowers
        self.template = template

    def __str__(self):
        print(self.borrowers)

    @send_data
    def send_passed_return_date(self, *args, **kwargs):  # smtp_server, port, sender_email, password, context):
        print('Before connected to SMTP server')
        try:
            print('connected to SMTP server')
            #
            with smtplib.SMTP_SSL(host=kwargs['smtp_server'], port=kwargs["port"], context=kwargs['context']) as server:
                for borrower in self.borrowers:
                    today = datetime.datetime.today()
                    today.strftime('%Y-%m-%d')
                    result = borrower.return_at - today
                    print(type(borrower.return_at))
                    mail = self.template.send_reminder_nearby().substitute(name=borrower.name, title=borrower.title,
                                                                         return_at=borrower.return_at, result=str(result))
                    #@TODO wysyla pustego maila
                    print('To jest mail:', mail)
                    print('Iterating threw self.borrowers')
                    server.login(kwargs['sender_email'], kwargs['password'])
                    print('logged in')
                    server.sendmail(kwargs['sender_email'], borrower.email, mail)

        except Exception as e:
            print(f'Error: {e}')
