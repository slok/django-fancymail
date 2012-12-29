import re

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import TemplateDoesNotExist


class FancyMail(EmailMultiAlternatives):
    """A Django EmailMessage (and EmailMultiAlternatives) simple subclass to
    help managing the template rendering more easily. It uses the default
    Django redering system.
    """

    def __init__(self, subject='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None, alternatives=None,
            cc=None):
        body = None
        self.html_template = None
        self.text_template = None
        self.context = None
        self.html_content = None
        super(FancyMail, self).__init__(subject, body, from_email,
                                to, bcc, connection, attachments, headers, cc)

    def load_template(self, html_template, context, text_template=None):
        """Loads the templates and creates the body of the html content and the
        template rendiring this one

        :param html_template: the HTML template to be rendered
        :param cotext: A dictionary with the context of the tempalte vars
        :param text_template: a plain template for the plain mail. This is
            optional, if nothing is passed then it will search a template with
            the same name as the html but with txt extension, If this neither
            doesn't exists then the tags will be removed from the rendered html
            template
        """
        self.html_template = html_template
        self.text_template = text_template
        self.context = context

        self._load_template()

    def _load_template(self):
        self.html_content = render_to_string(self.html_template, self.context)
        text_content = None

        # If there isn't txt template use the same name with txt extension
        if not self.text_template:
            text_template_match = re.match("(.*)(?=.html)", self.html_template)
            match = text_template_match.group(0)
            self.text_template = match + '.txt'
            try:
                text_content = render_to_string(self.text_template,
                                                self.context)
            except TemplateDoesNotExist:
                text_content = strip_tags(self.html_content)
        else:
            text_content = render_to_string(self.text_template, self.context)

        self.body = text_content
        self.attach_alternative(self.html_content, "text/html")

    def send(self, fail_silently=False):
        if not self.html_template or not self.context:
            raise AttributeError("First load the html template and context")

        # We have the templates but we haven't loaded to create the [html]body
        if not self.body or not self.html_content and\
            self.html_template and self.context:
            self._load_template()

        return super(FancyMail, self).send(fail_silently)


def send_mail(subject, html_template, context, from_email,
              recipient_list, text_template=None, fail_silently=False,
              auth_user=None, auth_password=None, connection=None):
    """Shortcut method to help sending emails"""

    msg = FancyMail(subject=subject, from_email=from_email, to=recipient_list)
    msg.load_template(html_template, context, text_template)
    msg.send()


def send_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    raise NotImplementedError()
