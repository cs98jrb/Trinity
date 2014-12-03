from django.conf.urls import patterns, url

from orders import views

urlpatterns = patterns('',
    # ex: /events/
    url(r'^$', views.index, name='orders'),
    # ex: /events/5/
    url(r'^(?P<order_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)