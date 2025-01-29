from django import forms
from .models import Model, SizeAmount, ProductionPiece


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model_number']
        widgets = {
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class SizeAmountForm(forms.ModelForm):
    class Meta:
        model = SizeAmount
        fields = ["size", "amount"]
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), 
        }
        
class ProductionPieceForm(forms.ModelForm):
    class Meta:
        model = ProductionPiece
        fields = ['used_amount']
        widgets = {
            'used_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), 
        }

class ProductionForm(forms.Form):
    model = forms.ModelChoiceField(
        queryset=Model.objects.all(),
        label="اختر الموديل",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    size_amount = forms.ChoiceField(
        label="اختر المقاس",
        choices=[("", "اختر المقاس")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    piece = forms.ChoiceField(
        label="اختر القطعة",
        choices=[("", "اختر القطعة")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    used_amount = forms.IntegerField(
        label="الكمية المراد استخدامها",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
