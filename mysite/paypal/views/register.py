import paypalrestsdk
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings

from orders.models import Order
from paypal.models import Payment


def register(request):
    """
    MyApp > Paypal > Create a Payment
    """

    # Check for open order
    if request.user.is_authenticated():
        open_order_list = Order.objects.open_order(user=request.user)
        if not open_order_list:
            return HttpResponse('<h2>No Order</h2>')
    else:
        return HttpResponse('<h2>Login Required</h2>')

    order = open_order_list[0]

    if order.total_ex == 0:
        order.open = False
        order.save()
        return HttpResponse('<h2>No Payment required</h2>')

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
            "return_url": request.build_absolute_uri(reverse("paypal:execute")),
            "cancel_url": request.build_absolute_uri(reverse('home page')) },
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

        register_pament = Payment(ref=payment.id,related_order=order,value=order.total_inc)
        register_pament.save()

        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        return HttpResponseRedirect(redirect_url)

    else:
        messages.error(request, 'We are sorry but something went wrong. We could not redirect you to Paypal.')
        return HttpResponse('<p>We are sorry but something went wrong. We could not redirect you to Paypal.</p><p>'+str(payment.error)+'</p>')
        #return HttpResponseRedirect(reverse('thank you'))
