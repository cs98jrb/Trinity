from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from events.models import Event
from orders.models import Order

@login_required
def index(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    order_list = Order.objects.filter(
        ordered_by=request.user
    )
    return render(request, 'orders/index.html', {
        'event_list': event_list,
        'order_list': order_list,
    })
