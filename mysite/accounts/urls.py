from django.conf.urls import patterns, url

from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.coming_soon, name='account'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
)