from django import forms
from .models import Artist

# Create your views here.
class SearchForm(forms.ModelForm):
    artist_name = forms.CharField(label='artist_name', max_length=100)

    class Meta:
        model = Artist
        fields = ['artist_name']
