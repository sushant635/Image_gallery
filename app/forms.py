from django import forms
from app.models import Album

class AlbumForm(forms.ModelForm):
   class Meta:
      models = Album
      exclude = []
   zip = forms.FileField(required=False)
    
    
