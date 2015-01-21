from django.conf.urls import patterns, url

from cms import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.index, name='index'),
    # ex: /events/
    url(r'^events/$', views.events, name='events'),
    # ex: /events/5/
    url(r'^events/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
    # ex: /events/5/
    url(r'^flatpage/(?P<page_url>\w+)/$', views.flatpage_detail, name='flatpage_detail'),
    # ex: /polls/5/results/
    # url(r'^(?P<event_id>\d+)/book/$', views.book, name='book'),
    # ex: /polls/5/vote/
    # url(r'^/thankyou/$', views.thankyou, name='thankyou'),
)