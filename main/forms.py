from .models import Catalog
from django.forms import ModelForm, ImageField, TextInput, NumberInput, FileInput, CheckboxInput, Select
from django import forms


class CatalogForm(ModelForm):
    photo = ImageField(widget=FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Catalog
        fields = ['title', 'price', 'photo', 'is_published', 'category']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter name"
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter price"
            }),
            'is_published': CheckboxInput(attrs={
                'class': 'required checkbox',
            }),
            'category': Select(attrs={
                'class': 'form-control',
            })
        }

