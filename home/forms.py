from django import forms
from . models import uimage

class ImageForm(forms.ModelForm):
    class Meta:
        model = uimage
        fields = ("caption","image")