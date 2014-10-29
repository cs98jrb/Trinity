from django.shortcuts import get_object_or_404, render
from events.models import Event

def index(request):
    event_list = Event.objects.order_by('pub_date')[:5]
    
    return render(request, 'events/index.html', {
        'event_list': event_list,
    })
    
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/detail.html', {'event': event})