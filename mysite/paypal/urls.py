from django.conf.urls import patterns, url

from paypal import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.register, name='register'),
    # ex: /events/5/
    url(r'^/execute/$', views.execute, name='execute'),
    url(r'^/cancel/$', views.cancel, name='cancel'),
)