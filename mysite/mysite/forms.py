from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from mysite.models import EmailInf


class ContactForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    confirm_email = forms.EmailField(
        max_length=254,
        label="Confirm email",
        required=True,
    )

    def __init__(self, request, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email
                self.fields['confirm_email'].initial = request.user.email
        except User.DoesNotExist:
            pass

    class Meta:
        model = EmailInf
        fields = ['name', 'email', 'confirm_email', 'message', ]

    def clean(self):

        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data


class CreateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Making first_name required
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    # set the css of required fields
    required_css_class = 'required'

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True
    )
    password2 = forms.CharField(
        label='Password', help_text='Confirm your password', widget=forms.PasswordInput, required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError(u'Username "%s" is already in use.' % username)

        return username

    def save(self, commit=True, login=True):
        # Hash the password
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

    def login(self, request):
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password1"])
        if user.is_active:
            login(request, user)
        else:
            raise ValidationError(u'Username "%s" is already in use.' % self.cleaned_data["username"])

        return user