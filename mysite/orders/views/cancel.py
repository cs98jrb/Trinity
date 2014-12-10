__author__ = 'james'
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Min, Sum, Count

from orders.models import Order
from events.models import Event

from orders.views import index


def cancel(request, order_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    order = get_object_or_404(Order, pk=order_id)

    order.delete(request)

    return index(request)
