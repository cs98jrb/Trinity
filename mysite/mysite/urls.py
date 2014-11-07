from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from mysite import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.IndexView.as_view(), name='home page'),
    
    #Event system
    url(r'^events/', include('events.urls', namespace="events")),

    #Holding pages
    url(r'^readings/', views.coming_soon, name='readings'),
    url(r'^books/', views.coming_soon, name='books'),
    url(r'^press/', views.coming_soon, name='press'),
    url(r'^serenity_centre/', views.coming_soon, name='serenity_centre'),
    url(r'^blog/', views.coming_soon, name='blog'),

    #the contact form.
    url(r'^contact/thanks', views.contact_thanks, name='thank you'),
    url(r'^contact/', views.get_contact, name='contact'),

    #actual site
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^events/', views.index, name='events'),
    #url(r'^readings/', views.index, name='readings'),
    #url(r'^books/', views.index, name='books'),
    #url(r'^press/', views.index, name='press'),
    #url(r'^serenity_centre/', views.index, name='serenity_centre'),
    #url(r'^blog/', views.index, name='blog'),
    #url(r'^contact/', views.index, name='contact'),
)
