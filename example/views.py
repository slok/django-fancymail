
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
            settings.EMAIL_HOST_USER = msg.from_email
            settings.EMAIL_HOST_PASSWORD = password

            #Set context
            context = {
                    'user': form.cleaned_data['context_user']
            }

            # Load templates
            msg.load_template("email/welcome.html", context)
            # Send!
            msg.send()

            messages.success(request,
                    "Mail sent to {0} ".format(context['user']))

    data = {
        'mail_form': MailForm(),
    }

    return render_to_response('example/index.html',
                            data,
                            context_instance=RequestContext(request))
