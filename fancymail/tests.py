import os
import shutil

from django.test import TestCase
from django.test.utils import override_settings

from fancymail.mail import send_mail

TMP_DIR = '/tmp/fancymail'


def read_single_file(path):
    file_path = path + "/" + os.listdir(path)[0]  # One file only
    f = open(file_path, "r")
    return "".join(f.readlines())


# Fake the email
@override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend')
@override_settings(EMAIL_FILE_PATH=TMP_DIR)
class MailTest(TestCase):

    CORRECT_TEXT = "Summary:\n\nThis is a test in Django and email with " +\
                "template using dancymail\n\n-------------------------------" +\
                "---------------\npowered by Python, Django and Django " +\
                "fancymail"

    CORRECT_HTML = "<html>\n    <head>\n    </head>\n    <body>\n" +\
                       "       \n        <h1>Summary</h1>\n        <div>" +\
                       "This is a test in Django and email with template " +\
                       "using dancymail</div>\n\n        <footer" +\
                       ">\n            powered by Python, Django and Django " +\
                       "fancymail\n        </footer>\n    </body>\n</html>"

    SUBJECT = "test"
    HTML_TEMPLATE = "test/test.html"
    TEXT_TEMPLATE = "test/test.txt"
    CONTEXT = {'main_title': "Test",
                   'title': "Summary",
                   'description': "This is a test in Django and email with template using dancymail"}
    FROM_EMAIL = "me@testfancymail.com"
    RECIPIENT_LIST = ["you@testfancymail.com", ]

    def tearDown(self):
        # Delete tmp dir
        shutil.rmtree(TMP_DIR)

    def test_send_mail(self):
        """Tests the send of an email with a HTML and text template"""

        send_mail(MailTest.SUBJECT,
            MailTest.HTML_TEMPLATE,
            MailTest.CONTEXT,
            MailTest.FROM_EMAIL,
            MailTest.RECIPIENT_LIST,
            MailTest.TEXT_TEMPLATE)

        # Check that is correct
        # 1 read email file
        email_file = read_single_file(TMP_DIR)

        # 2 Check headers data:
        content_type = "Content-Type: multipart/alternative;"
        subject = "Subject: {0}".format(MailTest.SUBJECT)
        sender = "From: {0}".format(MailTest.FROM_EMAIL)
        receiver = "To: {0}".format(MailTest.RECIPIENT_LIST[0])
        self.assertTrue(content_type in email_file)
        self.assertTrue(subject in email_file)
        self.assertTrue(sender in email_file)
        self.assertTrue(receiver in email_file)

        # 3 Check that there are 2 types of email (text and HTML)
        plain = 'Content-Type: text/plain; charset="utf-8"'
        html = 'Content-Type: text/html; charset="utf-8"'
        self.assertTrue(plain in email_file)
        self.assertTrue(html in email_file)

        # 4 Check text content
        self.assertTrue(MailTest.CORRECT_TEXT in email_file)

        # 5 Check html content
        self.assertTrue(MailTest.CORRECT_HTML in email_file)

    def test_send_mail_autofield_text_template(self):
        """Tests the seend_email but without especifing the text template so it
        will take the same name as the html with different extension
        """
        send_mail(MailTest.SUBJECT,
            MailTest.HTML_TEMPLATE,
            MailTest.CONTEXT,
            MailTest.FROM_EMAIL,
            MailTest.RECIPIENT_LIST)

        # Check that is correct
        # 1 read email file
        email_file = read_single_file(TMP_DIR)

        # 2 Check headers data:
        content_type = "Content-Type: multipart/alternative;"
        subject = "Subject: {0}".format(MailTest.SUBJECT)
        sender = "From: {0}".format(MailTest.FROM_EMAIL)
        receiver = "To: {0}".format(MailTest.RECIPIENT_LIST[0])
        self.assertTrue(content_type in email_file)
        self.assertTrue(subject in email_file)
        self.assertTrue(sender in email_file)
        self.assertTrue(receiver in email_file)

        # 3 Check that there are 2 types of email (text and HTML)
        plain = 'Content-Type: text/plain; charset="utf-8"'
        html = 'Content-Type: text/html; charset="utf-8"'
        self.assertTrue(plain in email_file)
        self.assertTrue(html in email_file)

        # 4 Check text content
        self.assertTrue(MailTest.CORRECT_TEXT in email_file)

        # 5 Check html content
        self.assertTrue(MailTest.CORRECT_HTML in email_file)

    def test_send_mail_autofield_text_template_with_strip_tags(self):
        """Tests the send_email but without especifing the text template so it
        will take the same name as the html without extension, but This
        doesn't exist so it strips the tags
        """
        send_mail(MailTest.SUBJECT,
            "test/test2.html",
            MailTest.CONTEXT,
            MailTest.FROM_EMAIL,
            MailTest.RECIPIENT_LIST)

        # Check that is correct
        # 1 read email file
        email_file = read_single_file(TMP_DIR)

        # 2 Check headers data:
        content_type = "Content-Type: multipart/alternative;"
        subject = "Subject: {0}".format(MailTest.SUBJECT)
        sender = "From: {0}".format(MailTest.FROM_EMAIL)
        receiver = "To: {0}".format(MailTest.RECIPIENT_LIST[0])
        self.assertTrue(content_type in email_file)
        self.assertTrue(subject in email_file)
        self.assertTrue(sender in email_file)
        self.assertTrue(receiver in email_file)

        # 3 Check that there are 2 types of email (text and HTML)
        plain = 'Content-Type: text/plain; charset="utf-8"'
        html = 'Content-Type: text/html; charset="utf-8"'
        self.assertTrue(plain in email_file)
        self.assertTrue(html in email_file)

        # 4 Check text content
        correct_text = "        Summary\n        This is a test in Django an" +\
        "d email with template using dancymail\n\n        \n            powe" +\
        "red by Python, Django and Django fancymail"

        self.assertTrue(correct_text in email_file)

        # 5 Check html content
        self.assertTrue(MailTest.CORRECT_HTML in email_file)
