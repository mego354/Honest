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
        required=True,  # The field is required
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    piece = forms.ChoiceField(
        label="اختر القطعة",
        required=True,  # The field is required
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    used_amount = forms.IntegerField(
        label="الكمية المراد استخدامها",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    def __init__(self, *args, **kwargs):
        # Dynamically populate size_amount and piece choices based on the selected model
        super().__init__(*args, **kwargs)
        
        if 'model' in self.data:  # Check if model has been selected (in a GET request or during form submission)
            model_id = self.data.get('model')
            model_instance = Model.objects.get(id=model_id)
            
            # Populate size_amount choices based on the model
            self.fields['size_amount'].choices = [
                (str(size.id), size.size) for size in model_instance.size_amounts.all()
            ]
            
            # Populate piece choices based on the model
            self.fields['piece'].choices = [
                (str(piece.id), piece.type) for piece in model_instance.pieces.all()
            ]
        else:
            # If no model is selected, set empty choices
            self.fields['size_amount'].choices = [("", "---------")]
            self.fields['piece'].choices = [("", "---------")]
    
