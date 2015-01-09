from django.conf import settings
from django.conf.urls import patterns, include, url


from django.contrib import admin
from mysite import views
from mysite import paypal


admin.autodiscover()

urlpatterns = patterns('django.contrib.flatpages.views',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', views.IndexView.as_view(), name='home page'),
    url(r'^$', 'flatpage', {'url': 'home/'}, name='home page'),
    url(r'^about/', views.about, name='about'),

    # Event system
    url(r'^events/', include('events.urls', namespace="events")),

    # Event system
    url(r'^order/', include('orders.urls', namespace="orders")),

    # Holding pages
    url(r'^terms/', views.tandc, name='tandc'),
    url(r'^privacy-policy/', views.privacy_policy, name='privacy'),
    url(r'^readings/', include('readings.urls', namespace='readings')),
    url(r'^books/', views.book, name='books'),
    url(r'^press/', views.press, name='press'),
    url(r'^serenity_centre/', views.serenity, name='serenity_centre'),
    url(r'^blog/', views.coming_soon, name='blog'),

    # the contact form.
    url(r'^contact/thanks', views.contact_thanks, name='thank you'),
    url(r'^contact/', views.get_contact, name='contact'),

    # Login
    url(r'^new_user/$', views.register, name='registration'),

    # actual site
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^sys_admin/', include(admin.site.urls)),

    url(r'^admin/', include('cms.urls', namespace='cms')),

    # paypal
    url(r'^paypal/', include('paypal.urls', namespace='paypal')),

    # testimonials
    url(r'^testimonials/', include('testimonials.urls', namespace='testimonials')),

    # Login
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),

    #Google
    url(r'^googlec35559684fb6219b.html', views.google),

    #cookie
    url(r'^cookies/', include('cookie_consent.urls')),

    #Flat pages
    (r'^pages/', include('django.contrib.flatpages.urls')),
)
