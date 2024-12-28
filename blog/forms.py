from django import forms
from .models import TravelPost

class TravelPostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = [
            'title', 'content', 'image', 'destination',
            'category', 'tags', 'published', 
            'meta_title', 'meta_description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta_title'].required = False
        self.fields['meta_description'].required = False

    def clean_meta_title(self):
        meta_title = self.cleaned_data.get('meta_title')
        if meta_title and len(meta_title) > 60:
            raise forms.ValidationError("El título meta no debe exceder los 60 caracteres.")
        return meta_title

    def clean_meta_description(self):
        meta_description = self.cleaned_data.get('meta_description')
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError("La descripción meta no debe exceder los 160 caracteres.")
        return meta_description

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'avatar']  # Incluye los campos que deseas editar

