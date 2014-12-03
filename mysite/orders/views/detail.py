__author__ = 'james'
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Min, Sum, Count

from orders.models import Order
from events.models import Event


def detail(request, order_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    order = get_object_or_404(Order, pk=order_id)

    vat_list = order.orderitem_set.order_by('vat').values('vat__rate').annotate(exvat=Sum('value'))
    for vat in vat_list:
        vat['incvat'] = round(vat['exvat'] * (1+vat['vat__rate']), 2)

    return render(request, 'orders/detail.html', {
        'event_list': event_list,
        'order': order,
        'vat_list': vat_list,
    })
