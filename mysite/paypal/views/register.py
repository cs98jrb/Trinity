import paypalrestsdk
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.conf import settings

from orders.models import Order
from paypal.models import Payment
from events.models import Event


def register(request, order_id=None):
    """
    MyApp > Paypal > Create a Payment
    """

    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    error = ''

    # check the order id
    order = None
    if order_id:
        order = Order.objects.get(id=order_id)
        if not order.open:
            error += '<p>Not an open order</p>'
    elif request.user.is_authenticated():# Check for open order
        open_order_list = Order.objects.open_order(user=request.user)
        if not open_order_list:
            error += '<p>No unpaid order</p>'
    else:
        error += '<p>You need to log in</p>'

    if error:
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': error,
        })

    # Close the order while taking payment
    if not order:
        order = open_order_list[0]
        order.waiting_payment = True
    print (order)

    try:
        order.save()
    except ValueError as e:
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': e,
        })

    if order.total_ex == 0:
        error += '<h2>No Payment required</h2>'
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': error,
        })

    #logging.basicConfig(level=logging.DEBUG)

    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET })

    # item_list format
    # {
    #    "items": [{
    #            "name": 127 char,
    #            "price": "xx.yy",
    #            "currency": "GBP",
    #            "quantity": int
    #        },
    #    ]},
    #    "amount":  {
    #        "total": "XX.YY",
    #        "currency": "GBP"
    #    }
    # }

    items = []

    for order_line in order.orderitem_set.all():
        line_entry = {
            "name": order_line.description,
            "price": "%.2f" % order_line.content_object.price.value_inc,
            "currency": "GBP",
            "quantity": order_line.content_object.quantity,
        }
        items.append(line_entry)

    payment_inf = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(),
            "cancel_url": request.build_absolute_uri(reverse('paypal:cancel')) },
        "transactions": [{
            "item_list": {
                "items": items
            },
            "amount":  {
                "total": "%.2f" % order.total_inc,
                "currency": "GBP"
            },
            "description": "Trinity Williams"
        }]
    }

    payment = paypalrestsdk.Payment(payment_inf)

    redirect_url = ""

    if payment.create():
        # Store payment id in user session
        request.session['payment_id'] = payment.id

        register_payment = Payment(ref=payment.id, related_order=order, value=order.total_inc)
        register_payment.save()

        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        return HttpResponseRedirect(redirect_url)

    else:
        messages.error(request, 'We are sorry but something went wrong. We could not redirect you to Paypal.')
        error += '<p>We are sorry but something went wrong. We could not redirect you to Paypal.</p><p>'+str(payment.error)+'</p>'
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': error,
        })
        #return HttpResponseRedirect(reverse('thank you'))
