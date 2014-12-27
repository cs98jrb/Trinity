
from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from paypal.models import Payment as PayPalPayment


def cancel(request):
    payment_id = False

    if 'payment_id' in request.session:
        payment_id = request.session['payment_id']
        del request.session['payment_id']
    else:
        html = "<p>No payment to cancel</p>"

    if payment_id:
        payment = PayPalPayment.objects.get(ref=payment_id)
        if payment:
            order = payment.related_order
            order.waiting_payment = False
            order.open = True
            order.save()
        html = "<p>Your payment has been canceled.</p>"


    return render(request, 'paypal/errors.html', {
        'error': html,
    })
