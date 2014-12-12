__author__ = 'james'
from django.utils import timezone
from events.models import Event
from testimonials.models import Testimonial

def event_list(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    return {
        'event_list': event_list,
    }

def test_list(request):
    testimonial = Testimonial.objects.filter(
        hompage = True
    ).order_by('?')[0]

    return {
        'testimonial': testimonial
    }