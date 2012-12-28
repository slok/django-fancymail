import re

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template import TemplateDoesNotExist


def send_mail(subject, html_template, context, from_email,
              recipient_list, text_template=None, fail_silently=False,
              auth_user=None, auth_password=None, connection=None):

    html_content = render_to_string(html_template, context)
    text_content = None

    # If there isn't txt template use the same name with txt extension
    if not text_template:
        text_template_match = re.match("(.*)(?=.html)", html_template)
        match = text_template_match.group(0)
        text_template = match + '.txt'
        try:
            text_content = render_to_string(text_template, context)
        except TemplateDoesNotExist:
            text_content = strip_tags(html_content)
    else:
        text_content = render_to_string(text_template, context)

    msg = EmailMultiAlternatives(subject=subject,
                                body=text_content,
                                from_email=from_email,
                                to=recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    raise NotImplementedError()
