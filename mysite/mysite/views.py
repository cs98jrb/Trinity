from django.shortcuts import render
from events.models import Event
from django.utils import timezone
from django import forms

from django.views import generic

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

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
