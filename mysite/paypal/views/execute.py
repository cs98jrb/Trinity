import paypalrestsdk
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings

from orders.models import Order, Payment, PaymentType
from paypal.models import Payment as PayPalPayment


def execute(request):
    """
    MyApp > Paypal > Execute a Payment
    """
    payment_id = request.session['payment_id']
    payer_id = request.GET['PayerID']

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
            order = order,
            type = PaymentType.objects.get(pk=1),
            payed = True,
            payment_ref = payment_id,
            value_inc = paypal_payment.value,
        )
        order_payment.save()
        order.open = False
        order.waiting_payment = False
        order.save()

        del request.session['payment_id']
        return HttpResponse('<p>the payment "'+payment_name+'" has been accepted</p>')
    else:
        # the payment is not valid
        # Re-open order as payment was not taken
        order.open = True
        order.waiting_payment = False
        order.save()
        del request.session['payment_id']
        return HttpResponse('<p>We are sorry but something went wrong. </p><p>'+str(payment.error)+'</p>')