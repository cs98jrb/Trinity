from django.shortcuts import render
from django.utils import timezone
from django import forms
from django.core.urlresolvers import reverse

from django.views import generic

from events.models import Event
from mysite.models import EmailInf

class IndexView(generic.ListView):
    template_name = 'mysite/index.html'
    def get_queryset(self):
        return Event.objects.filter(
            event_time__gte=timezone.now()
        )[:5]

def coming_soon(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    return render(request, 'mysite/coming_soon.html', {
        'event_list': event_list,
    })

def contact(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    
    
    return render(request, 'mysite/contact.html', {
        'event_list': event_list,
    })

class ContactForm(generic.CreateView):
    model = EmailInf
    template_name = 'mysite/contact.html'
    #form_class = forms.ContactForm
    def get_success_url(self):
        return reverse('home page')
    def get_context_data(self, **kwargs):
        context = super(ContactForm, self).get_context_data(**kwargs)
        context['event_list'] = Event.objects.filter(
            event_time__gte=timezone.now()
        )[:5]
        return context