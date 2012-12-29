from django.conf.urls import patterns, url

import example.views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', example.views.index, name='example-index'),
)
