from django import forms
from .models import Model, Piece, SizeAmount


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model_number']
        widgets = {
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

