from django.shortcuts import render
from events.models import Event

def index(request):
    event_list = Event.objects.order_by('pub_date')[:5]
    return render(request, 'mysite/index.html',  {
        'event_list': event_list,
    })

def coming_soon(request):
    context = {'title': ''}
    return render(request, 'mysite/coming_soon.html', context)