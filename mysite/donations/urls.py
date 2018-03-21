from django.conf.urls import patterns, url

from donations import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.make, name='make'),

)