from django import forms
from .models import Model, SizeAmount, ProductionPiece, Carton, Packing


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
    class Meta:
        model = ProductionPiece
        fields = ['used_amount', 'factory', 'comment']
        widgets = {
            'used_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'factory': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductionForm(forms.Form):
    model = forms.ModelChoiceField(
        queryset=Model.objects.filter(is_archive=False),
        label="اختر الموديل",
        # widget=forms.Select(attrs={'class': 'form-control'})
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'})
    )

    size_amount = forms.ChoiceField(
        label="اختر المقاس",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    piece = forms.ChoiceField(
        label="اختر القطعة",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    used_amount = forms.IntegerField(
        label="الكمية المراد استخدامها",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    factory = forms.CharField(
        label="اسم المصنع",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    comment = forms.CharField(
        label="الملاحظات",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
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

###############################################################################################################################
class PackingPieceForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ['used_carton', 'size_amount']
        widgets = {
            'used_carton': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
    
    size_amount = forms.ModelChoiceField(
        queryset=SizeAmount.objects.none(),  # Default empty queryset
        label="اختر المقاس",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instance = kwargs.get('instance')  # Get the instance if editing

        if instance and hasattr(instance, 'model') and hasattr(instance.model, 'size_amounts'):
            # Filter SizeAmount related to the Packing model
            sizes = SizeAmount.objects.filter(model=instance.model)  
            self.fields['size_amount'].queryset = sizes  # Assign queryset properly
            self.fields['size_amount'].label_from_instance = lambda obj: f"{obj.size} ({obj.Packing_per_carton})"
        else:
            self.fields['size_amount'].queryset = SizeAmount.objects.none()  # Default empty queryset

class PackingForm(forms.Form):
    model = forms.ModelChoiceField(
        queryset=Model.objects.filter(is_archive=False),
        label="اختر الموديل",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'display: none;'})
    )

    size_amount = forms.ChoiceField(
        label="اختر المقاس",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    carton = forms.ChoiceField(
        label="اختر الكرتونة",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    used_carton = forms.IntegerField(
        label="الكرتون للتعبئة",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )


    def __init__(self, *args, **kwargs):
        # Dynamically populate size_amount and piece choices based on the selected model
        super().__init__(*args, **kwargs)

        if 'model' in self.data:  # Check if model has been selected (in a GET request or during form submission)
            model_id = self.data.get('model')
            model_instance = Model.objects.get(id=model_id)

            # Populate choices based on the model
            self.fields['size_amount'].choices = [
                (str(size_amounts.id), f"{size_amounts.size} - {size_amounts.amount}") for size_amounts in model_instance.size_amounts.all()
            ]
            self.fields['carton'].choices = [
                (str(carton.id), f"{carton.length} -{carton.width} -{carton.height}") for carton in model_instance.cartons.all()
            ]
        else:
            # If no model is selected, set empty choices
            self.fields['size_amount'].choices = [("", "---------")]
            self.fields['carton'].choices = [("", "---------")]

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
