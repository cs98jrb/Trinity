from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.index, name='events'),
    # ex: /events/5/
    url(r'^(?P<event_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<event_id>\d+)/book/$', views.book, name='book'),
    # ex: /polls/5/vote/
    url(r'^thankyou/$', views.thankyou, name='thankyou'),
)