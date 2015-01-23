from django.conf.urls import patterns, url

from cms import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.index, name='index'),
    # ex: /events/
    url(r'^events/$', views.events, name='events'),
    # ex: /events/5/
    url(r'^events/new/$', views.event_add, name='event_add'),
    url(r'^events/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),

    url(r'^venue/new/$', views.venue_add, name='venue_add'),
    url(r'^venue/(?P<venue_id>\d+)/$', views.venue_detail, name='venue_detail'),

    url(r'^report/(?P<event_id>\d+)/$', views.event_report, name='event_report'),


    # ex: /events/5/
    url(r'^flatpage/(?P<page_url>\w+)/$', views.flatpage_detail, name='flatpage_detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<event_id>\d+)/book/$', views.book, name='book'),
    # ex: /polls/5/vote/
    # url(r'^/thankyou/$', views.thankyou, name='thankyou'),
)