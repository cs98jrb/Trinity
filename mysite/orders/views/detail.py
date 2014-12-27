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

    if request.method == 'POST':
        form = OrderDel(request, request.POST)
        if form.is_valid():
            email = order.ordered_by.email
            print(email)

            if form.cleaned_data['email'] == email:
                order.delete()
                return HttpResponseRedirect(reverse("home page"))
            else:
                form.add_error(
                    'email',
                    'This is not the correct email for this order.'
                )

    else:
        form = OrderDel(request)

    return render(request, 'orders/detail.html', {
        'order': order,
        'form': form,
    })
