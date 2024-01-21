from email.message import EmailMessage
from string import Template

class EmailTemplates():
    @staticmethod
    def send_reminder_overdue():
        # mssg = Template('$name, You have borrowed $title and return date passed $return_at\n Please return it imidietly\nBest Regards\nPawel')
        # return mssg
        # message = EmailMessage()
        # message.add_header('From', f'{sender}')
        # message.add_header('To', f'{borrower.email}')
        # message.add_header('Subject', 'Book return reminder')
        # body = f'''
        # Dear {borrower.name},
        #
        # You have borrowed {borrower.title} and return date passed {result}.
        # Please return it imidietly.
        #
        # Best Regards
        # Pawel
        # '''
        # message.set_content(body)
        # message_as_string = message.as_string()

        mssg = Template('''
        ... From: $sender_mail
        ... To: $borrower_email
        ... Subject: Book return reminder
     
        ... Dear $name, You have borrowed $title and return date passed $return_at
        ... Please return it imidietly.
        
        ... Best Regards
        ... Pawel ''')
        return mssg
    # @staticmethod
    # def send_reminder_nearby():
    #     # mssg = Template('$name, You have borrowed $title and the return day is $return_at. Its about @result days from today.Please try not to overdue this dateBest Regards'
    #     #                 'Pawel')
    #     # return mssg
    #     mssg = Template('''\
    #             ... From: $sender_mail
    #             ... Subject: Book return reminder
    #             ...
    #             ... $name, You have borrowed $title and return date will pass $return_at\n Its about $result days from today.Please try not to overdue this dateBest Regards ''')
    #     return mssg