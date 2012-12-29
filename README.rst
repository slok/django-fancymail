==================
Django Fancy mail
==================

Status
------

:Version:  0.1
:Tests: .. image:: https://api.travis-ci.org/slok/django-fancymail.png


Overview
--------

Fancy mail is a Django app to help managing your templated emails. The aim of
this app is to be simple and to reuse all the stuff that Django gives us, like
the email classes that works perfect (Thank you Django). There are alternatives
like `Django templated mail <https://github.com/bradwhittington/django-templated-email>`_. But this app has many options, like backends,
template renderers...

Fancy mail is more simple, you say where is the html template, what are the 
variables to use (context) and the text template (this is optional) and we are
done!

**Why use fancy mail?**

In two words: is simple!

**What comes in the box?**

You can use Fancy mail in two forms like the Django email. You can use the class
of ``FancyMail`` directly or you can use shortcuts

Dependencies
------------

- Django 1.4.*
- TODO: Test with 1.3.*

Quickstart
----------

Install
=======

TODO ``setup.py``

Prepare the templates
=====================

Fancy mail uses de Dajngo renderer for the templates so by default this uses
the template loader.

Add to the template loader in our settings ``TEMPLATE_LOADERS`` var this:

.. code-block:: python
    
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

Now we need to add the directory where our templates are. For example in the 
root directory of our app we will place a directory called ``email_templates``
with this estructure::

    ./email_templates/
    |
    `-- email
        |-- base.html
        |-- base.txt
        |-- welcome.html
        `-- welcome.txt

So we add in the settings ``TEMPLATE_DIRS`` this 
(in production add full path not relative):

.. code-block:: python

    'email_templates/'

We are ready to use it!

Use Directly
============

Using the class directoly (this has more options, the same options that the
Django documentation explains for EmailMultiAlternatives and EmailMessage)


First import:

.. code-block:: python

    from fancymail.mail import FancyMail 

then you need to create an instance of FancyMail with the needed data:

.. code-block:: python

    msg = FancyMail(subject="This is a test email", 
                from_email="test1@djangofancymail.org",
                to=("test2@djangofancymail.org",))


Then you need to load the templates:

.. code-block:: python

    msg.load_template("email/welcome.html", {'user': "slok"}, "email/welcome.txt")

OR set in the instance (when send the templates will be rendered) if you prefer:

.. code-block:: python

    msg.html_template = "email/welcome.html"
    msg.context = {'user': "slok"}
    msg.text_template = "email/welcome.txt"

Send the email!:

.. code-block:: python

    msg.send()

simple and easy :)


Use with Shortcuts
==================

Even simpler!:

.. code-block:: python

    send_mail("This is a test email", "email/welcome.html", {'user': "slok"},
            "test1@djangofancymail.org", ("test2@djangofancymail.org",), 
            "email/welcome.txt")

TODO
----

- Documentation
- more shortcuts

Author
------

`Xabier (slok) Larrakoetxea <http://xlarrakoetxea.org>`_ <slok69 [at] gmail.com>

License
-------

3 clause/New BSD license `OpenSource <http://www.opensource.org/licenses/BSD-3-Clause>`_, `Wikipedia <http://en.wikipedia.org/wiki/BSD_licenses>`_,
