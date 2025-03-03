from rest_framework import serializers
from .models import Model, SizeAmount, Piece, ProductionPiece, Carton, Packing

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class SizeAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeAmount
        fields = '__all__'

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = '__all__'

class ProductionPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPiece
        fields = '__all__'

class CartonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carton
        fields = '__all__'

class PackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packing
        fields = '__all__'