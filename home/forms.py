from django import forms
from .models import UserUploadedImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = UserUploadedImage
        fields = ("caption","image")