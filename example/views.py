
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext
from django.contrib import messages
from fancymail.mail import FancyMail

from example.forms import MailForm


def index(request):

    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():

            #Create the email
            msg = FancyMail()
            msg.subject = form.cleaned_data['subject']
            msg.to = [form.cleaned_data['to'], ]
            msg.from_email = form.cleaned_data['from_email']
            password = form.cleaned_data['password']
            use_tls = form.cleaned_data['use_tls']
            email_host = form.cleaned_data['email_host']
            email_port = form.cleaned_data['email_port']

            # Set Django live settings (Do not do this in production!!!!)
            settings.EMAIL_HOST_USER = msg.from_email
            settings.EMAIL_HOST_PASSWORD = password
            settings.EMAIL_USE_TLS = use_tls
            settings.EMAIL_HOST = email_host
            settings.EMAIL_PORT = email_port

            #Set context
            context = {
                    'user': form.cleaned_data['context_user']
            }

            # Load templates
            template = form.cleaned_data['template']
            msg.load_template("email/{0}/welcome.html".format(template),
                                context)
            # Send!
            msg.send()

            messages.success(request,
                    "Mail sent to {0} ".format(context['user']))
    else:
        form = MailForm()

    data = {
        'mail_form': form,
    }

    return render_to_response('example/index.html',
                            data,
                            context_instance=RequestContext(request))
