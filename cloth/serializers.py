from rest_framework import serializers
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics

class FabricSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Fabric
        fields = '__all__'

class CutTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CutTransfer
        fields = '__all__'

class ReturnTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ReturnTransfer
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Statistics
        fields = '__all__'
