import paypalrestsdk

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET

def paypal_create(request):
    """
    MyApp > Paypal > Create a Payment
    """
    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal" },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('paypal_execute')),
            "cancel_url": request.build_absolute_uri(reverse('home page')) },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "name of your item",
                    "price": "10",
                    "currency": "GBP",
                    "quantity": 1 }]},
            "amount":  {
                "total": "total price",
                "currency": "GBP" },
            "description": "purchase description" }]})

    redirect_url = request.build_absolute_uri(reverse('thank you'))

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
        return HttpResponseRedirect(reverse('thank you'))


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
    payment_name = payment.transactions[0].item_list.items[0].name

    #if payment.execute({"payer_id": payer_id}):
        # the payment has been accepted
    #else:
        # the payment is not valid


    return HttpResponseRedirect(reverse('thank you'))