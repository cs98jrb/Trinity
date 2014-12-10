from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from events.models import Event, Booking
from orders.models import Order

@login_required
def index(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    #order_list = Order.objects.filter(
    #    ordered_by=request.user
    #)

    order_list = Order.objects.filter(
        ordered_by=request.user
    )[:10]

    bookings = []

    booking_list = Booking.objects.filter(
        booked_by=request.user
    )
    if booking_list:
        for booking in booking_list:
            bookings.append({
                'date': booking.event.event_time,
                'venue': booking.event.venue,
                'num_people': booking.quantity,
                'ref': booking.ref
                })


    return render(request, 'orders/index.html', {
        'event_list': event_list,
        'order_list': order_list,
        'bookings': bookings,
    })
