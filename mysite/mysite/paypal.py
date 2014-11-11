import paypalrestsdk
import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

def paypal_create(request):
    """
    MyApp > Paypal > Create a Payment
    """

    logging.basicConfig(level=logging.DEBUG)

    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('paypal_execute')),
            "cancel_url": request.build_absolute_uri(reverse('home page')) },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "name of your item 1",
                    "price": "10.00",
                    "currency": "GBP",
                    "quantity": 1,
                    "sku": "1"
                }, {
                    "name": "name of your item 2",
                    "price": "10.00",
                    "currency": "GBP",
                    "quantity": 1,
                    "sku": "2"
                }]},
            "amount":  {
                "total": "20.00",
                "currency": "GBP"
            },
            "description": "purchase description"
        }]
    })

    redirect_url = ""

    if payment.create():
        # Store payment id in user session
        request.session['payment_id'] = payment.id

        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        return HttpResponseRedirect(redirect_url)

    else:
        messages.error(request, 'We are sorry but something went wrong. We could not redirect you to Paypal.')
        return HttpResponse('<p>We are sorry but something went wrong. We could not redirect you to Paypal.</p><p>'+str(payment.error)+'</p>')
        #return HttpResponseRedirect(reverse('thank you'))


def paypal_execute(request):
    """
    MyApp > Paypal > Execute a Payment
    """
    payment_id = request.session['payment_id']
    payer_id = request.GET['PayerID']

    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment.find(payment_id)
    payment_name = payment.transactions[0].description

    if payment.execute({"payer_id": payer_id}):
        # the payment has been accepted
        return HttpResponse('<p>the payment "'+payment_name+'" has been accepted</p>')
    else:
        # the payment is not valid
        return HttpResponse('<p>We are sorry but something went wrong. </p><p>'+str(payment.error)+'</p>')
