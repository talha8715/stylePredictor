from django import forms
from .models import Post, Comment
from .snippets import choice1, choice2

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter title'}))

    categories = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description'}))

    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    tag = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=choice1)

    event = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=choice2)

    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title','image','categories','tag','event','details']
