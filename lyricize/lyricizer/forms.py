from django import forms


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
