from django import forms


CHOICES = [('template1', 'Template 1'),
          ('template2', 'Template 2'),
          ('template2', 'Template 3')]


class MailForm(forms.Form):
    template = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField(max_length=200, label=u'Subject')
    to = forms.EmailField(max_length=200, label=u'To')
    from_email = forms.EmailField(max_length=200, label=u'From')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                max_length=50, label=u'Password')

    context_user = forms.CharField(max_length=50, label=u'email template user')
