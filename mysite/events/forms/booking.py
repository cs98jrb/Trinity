__author__ = 'james'
from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from events.models import Booking

from orders.models import Order, OrderItem


class BookingForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        booking = super(BookingForm, self).__init__(*args, **kwargs)

        # add label
        self.fields['quantity'].label = "Number of people"

    class Meta:
        model = Booking
        fields = ['quantity', ]

    def save(self, event, price, user, commit=True):
        from django.contrib.contenttypes.models import ContentType
        #
        booking = super(BookingForm, self).save(commit=False)

        booking.booked_by = user
        booking.event = event
        booking.price = price
        total_booked = 0
        open_order_list = Order.objects.open_order(user=user)
        if open_order_list:
            order = open_order_list[0]

            for item in order.orderitem_set.all():
                total_booked += item.content_object.quantity

        if not(event.pricing_set.all().filter(online_book=True)
                and not event.fully_booked):
            raise ValidationError(
                _('This event is fully booked'),
                code='Fully Booked'
            )
            commit = False
        elif event.num_spaces < (booking.quantity + total_booked):
            places = booking.quantity + total_booked
            raise ValidationError(
                _('Not enough spaces for %(places)s people.'),
                code='No Space',
                params={'places': places},
            )
            commit = False

        if commit:
            booking.save()

            # Add to open order
            if not open_order_list:
                order = Order(ordered_by=user)

            order.save()

            order_item = OrderItem(
                order=order,
                description=event.__unicode__(),
                value=(price.value*booking.quantity),
                vat=price.vat,
                content_type=ContentType.objects.get_for_model(booking),
                object_id=booking.id
            )

            order_item.save()

        return booking

    def clean(self):
        return self.cleaned_data