from django.conf.urls import patterns, url

from paypal import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.register, name='register'),
    # ex: /events/5/
    #url(r'^(?P<order_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<order_id>\d+)/pay/$', views.pay, name='pay'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)