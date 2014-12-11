import paypalrestsdk
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from orders.models import Order, Payment, PaymentType
from paypal.models import Payment as PayPalPayment
from events.models import Event

def execute(request):
    """
    MyApp > Paypal > Execute a Payment
    """

    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    if 'payment_id' in request.session:
        payment_id = request.session['payment_id']
        payer_id = request.GET['PayerID']
    else:
        error = '<p>We are sorry but something went wrong.</p>'
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': error,
        })

    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id":  settings.PAYPAL_CLIENT_ID,
        "client_secret":  settings.PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment.find(payment_id)
    payment_name = payment.transactions[0].description

    # Get payment from DB
    paypal_payment = PayPalPayment.objects.get(ref=payment_id)

    # get related order
    order = paypal_payment.related_order
    if payment.execute({"payer_id": payer_id}):
        # the payment has been accepted

        # Create order payment
        order_payment = Payment(
            order=order,
            type=PaymentType.objects.get(pk=1),
            payed=True,
            payment_ref=payment_id,
            value_inc=paypal_payment.value,
        )
        order_payment.save()
        order.open = False
        order.waiting_payment = False
        order.save()

        del request.session['payment_id']

        html = "<p>Thank you for your payment. A confirmation email has been sent containing your order details</p>"
        return render(request, 'paypal/success.html', {
            'event_list': event_list,
            'html': html,
        })
    else:
        # the payment is not valid
        # Re-open order as payment was not taken
        order.open = True
        order.waiting_payment = False
        order.save()
        del request.session['payment_id']

        error = '<p>We are sorry but something went wrong.</p>' \
                '<p>'+str(payment.error)+'</p>'
        return render(request, 'paypal/errors.html', {
            'event_list': event_list,
            'error': error,
        })