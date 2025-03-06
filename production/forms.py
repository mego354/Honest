from django import forms
from .models import Factory, Model, SizeAmount, ProductionPiece, Carton, Packing


class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['model_number']
        widgets = {
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

###############################################################################################################################
class SizeAmountForm(forms.ModelForm):
    class Meta:
        model = SizeAmount
        fields = ["size", "amount", 'Packing_per_carton']
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'Packing_per_carton': forms.Select(attrs={'class': 'form-control'}), 
        }

###############################################################################################################################
class ProductionPieceForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worked_factory'].queryset = Factory.objects.filter(statue__lt=2)
        
    class Meta:
        model = ProductionPiece
        fields = ['used_amount', 'worked_factory', 'comment']
        widgets = {
            'used_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'worked_factory': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductionForm(forms.Form):
    model = forms.ModelChoiceField(
        queryset=Model.objects.filter(is_archive=False),
        label="اختر الموديل",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'})
    )

    piece = forms.ChoiceField(
        label="اختر القطعة",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    worked_factory = forms.ModelChoiceField(
        queryset=Factory.objects.filter(statue__lt=2),
        label="اسم المصنع",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        # Dynamically populate size_amount and piece choices based on the selected model
        super().__init__(*args, **kwargs)

        if 'model' in self.data:  # Check if model has been selected (in a GET request or during form submission)
            model_id = self.data.get('model')
            model_instance = Model.objects.get(id=model_id)

            # Populate piece choices based on the model
            piece_types = set([piece.type for piece in model_instance.pieces.all()])
            self.fields['piece'].choices = [(piece_type, piece_type) for piece_type in piece_types]
        else:
            # If no model is selected, set empty choices
            self.fields['piece'].choices = [("", "---------")]
            
###############################################################################################################################
class PackingPieceForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ['used_carton', 'carton']
        widgets = {
            'used_carton': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
    
    carton = forms.ModelChoiceField(
        queryset=Carton.objects.none(),  # Default empty queryset
        label="اختر الكرتونة",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instance = kwargs.get('instance')  # Get the instance if editing

        if instance and hasattr(instance, 'model'):
            # Filter SizeAmount related to the Packing model
            cartons = Carton.objects.filter(model=instance.model)  
            self.fields['carton'].queryset = cartons  # Assign queryset properly
            self.fields['carton'].label_from_instance = lambda obj: f"{obj.length}*{obj.width}*{obj.height} ({obj.type})"
        else:
            self.fields['carton'].queryset = Carton.objects.none()  # Default empty queryset
    
class PackingForm(forms.Form):
    model = forms.ModelChoiceField(
        queryset=Model.objects.filter(is_archive=False),
        label="اختر الموديل",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'})
    )

###############################################################################################################################
class CartonForm(forms.ModelForm):
    class Meta:
        model = Carton
        fields = ['length', 'width', 'height', 'type', 'comment']
        widgets = {
            'length' : forms.TextInput(attrs={'class': 'form-control'}),
            'width'  : forms.TextInput(attrs={'class': 'form-control'}),
            'height' : forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }
