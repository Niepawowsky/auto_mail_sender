import datetime
import smtplib, ssl
from dotenv import load_dotenv
from os import environ, getenv
from string import Template

from templates.template_render import EmailTemplates


class MailSender():

    @staticmethod
    def send_data(func):
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

    def __init__(self, borrowers: list, template: EmailTemplates):
        self.borrowers = borrowers
        self.template = template

    def __str__(self):
        print(self.borrowers)

    @send_data
    def send_passed_return_date(self, *args, **kwargs):  # smtp_server, port, sender_email, password, context):
        print('Before connected to SMTP server')
        sender = kwargs['sender_email']
        password = kwargs['password']

        try:
            print('connected to SMTP server')
            #
            with smtplib.SMTP_SSL(host=kwargs['smtp_server'], port=kwargs["port"], context=kwargs['context']) as server:
                for borrower in self.borrowers:
                    today = datetime.datetime.today()
                    today.strftime('%Y-%m-%d')
                    result = borrower.return_at - today
                    result = str(result.days)
                    print(type(borrower.return_at))
                    # mail = self.template.send_reminder_overdue().
                    mail = self.template.send_reminder_overdue().substitute(sender_mail=sender,name=borrower.name, title=borrower.title,
                                                                         return_at=borrower.return_at, borrower_email=borrower.email, result=result)
                    #@TODO wysyla pustego maila
                    print('To jest mail:', mail)
                    print('Iterating threw self.borrowers')
                    server.login(sender, password)
                    print('logged in')
                    server.sendmail(from_addr=sender, to_addrs=borrower.email, msg=mail)
                    print('email sent')

        except Exception as e:
            print(f'Error: {e}')
