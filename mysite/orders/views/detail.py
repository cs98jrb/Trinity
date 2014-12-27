__author__ = 'james'
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Min, Sum, Count

from orders.models import Order
from orders.forms import OrderDel

def detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    return render(request, 'orders/detail.html', {
        'order': order
    })
