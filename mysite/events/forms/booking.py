__author__ = 'james'
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
        super(BookingForm, self).__init__(*args, **kwargs)
        # Making first_name required
        self.fields['quantity'].label = "Number of people"

    # def __init__(self, request, *args, **kwargs):
    #    super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['quantity', ]

    def save(self, event, price, user):
        from django.contrib.contenttypes.models import ContentType
        # Hash the password
        booking = super(BookingForm, self).save(commit=False)
        booking.event = event
        booking.price = price
        booking.save()

        # Add to open order
        open_order_list = Order.objects.open_order(user=user)
        if open_order_list:
            order = open_order_list[0]
        else:
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