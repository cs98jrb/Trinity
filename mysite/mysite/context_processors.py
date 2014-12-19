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
    testimonial_list = Testimonial.objects.filter(
        hompage = True
    )

    if len(testimonial_list) > 0:
        testimonial = testimonial_list.order_by('?')[0]
    else:
        testimonial = None

    return {
        'testimonial': testimonial
    }


def dnt_request(request):
    return {
        'tracking': not request.DNT
    }