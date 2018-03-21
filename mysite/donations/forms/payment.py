from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


from orders.models import Order, OrderItem
from donations.models import Pricing, Donation


class PaymentForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'
    email = forms.EmailField(
        max_length=254,
        label="Email address",
        required=True,
        help_text="This is required so we can contact you."
    )

    donation_val = forms.DecimalField(label='Value', min_value=1, max_digits=7, decimal_places=2)

    tandc = forms.BooleanField(
        label="Accept terms and conditions",
        required=True,
    )

    class Meta:
        model = Donation
        fields = ['email', ]

    def __init__(self, request, *args, **kwargs):
        donation = super(PaymentForm, self).__init__(*args, **kwargs)

        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email

        except User.DoesNotExist:
            pass


    def save(self, user, value, commit=True):
        from django.contrib.contenttypes.models import ContentType

        pricing = Pricing()

        pricing.value = value

        pricing.save()

        donation = super(PaymentForm, self).save(commit=False)

        donation.price = pricing

        donation.booked_by = user
        open_order_list = Order.objects.open_order(user=user)
        if open_order_list:
            order = open_order_list[0]

        if commit:
            donation.save()

            # Add to open order
            if not open_order_list:
                order = Order(ordered_by=user)

            order.save()

            order_item = OrderItem(
                order=order,
                description=donation.__unicode__(),
                value=(pricing.value*donation.quantity),
                vat=donation.price.vat,
                content_type=ContentType.objects.get_for_model(donation),
                object_id=donation.id
            )

            order_item.save()

        return pricing

    def clean(self):
        return self.cleaned_data