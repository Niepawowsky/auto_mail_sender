"""
This modul maintain messages used in mail_sender.py module.
Python email.message library is used here
In the future there should be jinja2 templates.
"""

from email.message import EmailMessage


class EmailTemplates():
    """
    Class that maintan messages for following scenario:
    1. Somebody passed the date of return
    2. Someone's return date is later than today.
    """
    @staticmethod
    def send_reminder_overdue(sender_mail, borrower_email, name, title, return_at, subject):

        """
        The send_reminder_overdue function takes in the following arguments:
        sender_mail - a string representing the email address of the sender
        borrower_email - a string representing
        the email address of who borrowed an item from you
        name - a string representing their name (first or last)
        title - a string representing what they borrowed from you
        return_at - an integer that represents when they should have returned it to you by now.

        :param sender_mail: Set the sender's email address
        :param borrower_email: Send the email to a specific person
        :param name: Personalize the message
        :param title: Specify the title of the book
        :param return_at: Pass the date when the book should be returned
        :param subject: Set the subject of the email
        :return: A message object
        :doc-author: Trelent
        """
        mssg = EmailMessage()
        mssg.set_content(f'''
        Dear {name}, 
        
        You have borrowed {title} and return date passed {return_at}.
        Please return it immediately.
        Best Regards,
        Pawel''')
        mssg["Subject"] = subject
        mssg["From"] = sender_mail
        mssg["To"] = borrower_email

        return mssg

    @staticmethod
    def send_reminder_nearby(sender_mail, borrower_email, name, title, return_at, subject):

        """
        The send_reminder_nearby function sends an email to the borrower of a book that is due soon.
        The function takes in the following arguments:
            sender_mail (str): The email address of the person sending this reminder.
            borrower_email (str): The email address of the person who borrowed this book.
            name (str): The first name of the person who borrowed this book,
            for personalization purposes.
            This should be retrieved from your database using SQLAlchemy's query functionality!

        :param sender_mail: Set the sender's email address
        :param borrower_email: Send the email to the borrower
        :param name: Personalize the message
        :param title: Specify the title of the book that is borrowed
        :param return_at: Get the return date of a book
        :param subject: Set the subject of the email
        :return: The mssg variable
        :doc-author: Trelent
        """
        mssg = EmailMessage()
        mssg.set_content(f'''
            Dear {name}, You have borrowed {title} and return date is {return_at}
            Please remember to return it on time.
            Best Regards
            Pawel ''')
        mssg["Subject"] = subject
        mssg["From"] = sender_mail
        mssg["To"] = borrower_email

        return mssg
