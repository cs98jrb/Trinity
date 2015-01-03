__author__ = 'james'
from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from readings.models import Booking

from orders.models import Order, OrderItem


class BookingForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'
    email = forms.EmailField(
        max_length=254,
        label="Contact email",
        required=True,
        help_text="This is required so we can contact you."
    )

    tandc = forms.BooleanField(
        label="Accept terms and conditions",
        required=True,
    )



    class Meta:
        model = Booking
        fields = ['email', 'price', 'quantity', ]

    def __init__(self, request, *args, **kwargs):
        booking = super(BookingForm, self).__init__(*args, **kwargs)

        # add label
        self.fields['price'].label = "Reading type"
        self.fields['quantity'].label = "Number of people"

        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email

        except User.DoesNotExist:
            pass


    def save(self, user, commit=True):
        from django.contrib.contenttypes.models import ContentType
        #
        booking = super(BookingForm, self).save(commit=False)

        booking.booked_by = user
        open_order_list = Order.objects.open_order(user=user)
        if open_order_list:
            order = open_order_list[0]

        if commit:
            booking.save()

            # Add to open order
            if not open_order_list:
                order = Order(ordered_by=user)

            order.save()

            order_item = OrderItem(
                order=order,
                description=booking.price.__unicode__(),
                value=(booking.price.value*booking.quantity),
                vat=booking.price.vat,
                content_type=ContentType.objects.get_for_model(booking),
                object_id=booking.id
            )

            order_item.save()

        return booking

    def clean(self):
        return self.cleaned_data