from rest_framework import serializers
from .models import Model, SizeAmount, Piece, ProductionPiece, Carton, Packing


class VerboseNameSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        new_representation = {}

        for field_name, value in representation.items():
            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                field_label = model_field.verbose_name
            except :
                field_label = field_name.replace('_', ' ').capitalize()
            
            new_representation[field_label] = value
        
        return new_representation
    
class ModelSerializer(VerboseNameSerializer):
    model_usage = serializers.SerializerMethodField()

    class Meta:
        model = Model
        fields = '__all__'  # This alone does not include model_usage
        fields = ['id', 'model_number', 'created_at', 'ended_at', 'shipped_at', 
                  'is_archive', 'is_shipped', 'available_carton', 'used_carton', 'model_usage']

    def get_model_usage(self, obj):
        return obj.get_model_usage()

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