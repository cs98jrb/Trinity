from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from orders.models import Order


class OrderDel(forms.Form):
    # set the css of required fields
    required_css_class = 'required'
    email = forms.EmailField(
        required=True,
        label="Order email address",
        help_text="This is required to confirm that this is your order."
    )

    def __init__(self,request, *args, **kwargs):
        super(OrderDel, self).__init__(*args, **kwargs)
        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email
        except User.DoesNotExist:
            pass

    class Meta:
        fields = ['email',]

    def clean(self):
        return self.cleaned_data