from django import forms


CHOICES = [('template1', 'Template 1'),
          ('template2', 'Template 2')]


class MailForm(forms.Form):
    template = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField(max_length=200, label=u'Subject')
    to = forms.EmailField(max_length=200, label=u'To')
    from_email = forms.EmailField(max_length=200, label=u'From')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                max_length=50, label=u'Password')

    context_user = forms.CharField(max_length=50, label=u'Personalized name')

    email_host = forms.CharField(max_length=50, label=u'Email host')
    email_port = forms.IntegerField(label=u'Email port')
    use_tls = forms.BooleanField(label=u'Use TLS', initial=False, required=False)
    use_gmail = forms.BooleanField(label=u'Use Gmail settings', initial=False, required=False)
