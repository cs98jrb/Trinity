from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from events.models import Event

from events.forms import BookingForm


def index(request):
    Event.capacity = 1
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    return render(request, 'events/index.html', {
        'event_list': event_list,
    })


def detail(request, event_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    event = get_object_or_404(Event, pk=event_id)
    if event.pricing_set.all().filter(online_book=True)\
            and not event.fully_booked:
        booking = True
    else:
        booking = False

    return render(request, 'events/detail.html', {
        'event_list': event_list,
        'event': event,
        'bookable': booking,
        'request': request,
        'form': BookingForm(),
    })

@login_required
def book(request, event_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    event = get_object_or_404(Event, pk=event_id)
    pricing_set = event.pricing_set
    online_pricing = event.pricing_set.all().filter(online_book=True)
    pricing = online_pricing[0]

    if event.pricing_set.all().filter(online_book=True)\
            and not event.fully_booked:
        booking = True
    else:
        booking = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            from orders.models import Order
            # process the data in form.cleaned_data as required

            try:
                form.save(event=event, price=pricing, user=request.user)
                open_order = Order.objects.open_order(request.user)

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('orders:detail', kwargs={'order_id': open_order[0].id}))
            except ValidationError as e:
                form.add_error('quantity', e)


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookingForm()

    return render(request, 'events/detail.html', {
        'event_list': event_list,
        'event': event,
        'bookable': booking,
        'request': request,
        'form': form,
    })


def thankyou(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    return render(request, 'events/thankyou.html', {
        'event_list': event_list,
    })