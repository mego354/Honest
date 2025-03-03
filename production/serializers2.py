from rest_framework import serializers
from .models import Model, SizeAmount, Piece, ProductionPiece, Carton, Packing


class VerboseNameSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Convert field names to their verbose_name
        representation = super().to_representation(instance)
        new_representation = {}
        for field_name, value in representation.items():
            model_field = self.Meta.model._meta.get_field(field_name)
            new_representation[model_field.verbose_name] = value
        return new_representation
    
class ModelSerializer(VerboseNameSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class SizeAmountSerializer(VerboseNameSerializer):
    class Meta:
        model = SizeAmount
        fields = '__all__'

class PieceSerializer(VerboseNameSerializer):
    class Meta:
        model = Piece
        fields = '__all__'

class ProductionPieceSerializer(VerboseNameSerializer):
    class Meta:
        model = ProductionPiece
        fields = '__all__'

class CartonSerializer(VerboseNameSerializer):
    class Meta:
        model = Carton
        fields = '__all__'

class PackingSerializer(VerboseNameSerializer):
    class Meta:
        model = Packing
        fields = '__all__'