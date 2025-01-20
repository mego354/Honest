from django import forms
from .models import Model, Piece, SizeAmount


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model_number']
        widgets = {
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DynamicPieceForm(forms.Form):
    def __init__(self, pieces_count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(pieces_count):
            self.fields[f'piece_name_{i+1}'] = forms.CharField(
                label=f'Piece Name {i+1}', max_length=50, required=True
            )


class SizeAmountForm(forms.Form):
    size = forms.CharField(label="Size", max_length=50, required=True)
    amount = forms.IntegerField(label="Amount", required=True)
