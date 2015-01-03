from django.conf.urls import patterns, url

from readings import views

urlpatterns = patterns('',

    url(r'^$', views.reading, name='book'),

    url(r'^payment/$', views.book, name='payment'),
    # ex: /polls/5/vote/
    url(r'^thankyou/$', views.thankyou, name='thankyou'),
)