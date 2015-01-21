__author__ = 'james'

from django import forms
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget

class UpdateFlatPage(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = [
            'title',
            'content',
            ]

    def clean(self):
        return self.cleaned_data