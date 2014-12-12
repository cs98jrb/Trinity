from django.conf.urls import patterns, url

from testimonials import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.index, name='index'),
    # ex: /events/5/
    url(r'^(?P<test_id>\d+)/$', views.detail, name='detail'),
)