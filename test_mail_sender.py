import pytest
from string import Template
from templates.template_render import EmailTemplates
from mail_sender import MailSender
from database.db_service import DbManager, DataBaseService
import sqlite3


def test_email_send():
    mssg = Template('This is test message')



