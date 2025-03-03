from rest_framework import serializers
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics

class VerboseNameSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # Convert field names to their verbose_name
        representation = super().to_representation(instance)
        new_representation = {}
        for field_name, value in representation.items():
            model_field = self.Meta.model._meta.get_field(field_name)
            new_representation[model_field.verbose_name] = value
        return new_representation

    
class FabricSerializer(VerboseNameSerializer):
    class Meta:
        model = Fabric
        fields = '__all__'

    def create(self, validated_data):
        instance, created = Fabric.objects.get_or_create(
            fabric_code=validated_data.get('fabric_code'),
            defaults=validated_data  # Use provided data if creating a new entry
        )
        if not created:
            # Update existing entry
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

class CutTransferSerializer(VerboseNameSerializer):
    class Meta:
        model = CutTransfer
        fields = '__all__'

    def create(self, validated_data):
        # Ensure ID is not manually assigned
        validated_data.pop("id", None)

        instance, created = CutTransfer.objects.get_or_create(
            fabric_code=validated_data.get('fabric_code'),
            model_number=validated_data.get('model_number'),
            defaults=validated_data
        )
        if not created:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

class ReturnTransferSerializer(VerboseNameSerializer):
    class Meta:
        model = ReturnTransfer
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop("id", None)  # Remove manually assigned ID

        instance, created = ReturnTransfer.objects.get_or_create(
            fabric_code=validated_data.get('fabric_code'),
            model_number=validated_data.get('model_number'),
            defaults=validated_data
        )
        if not created:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance

class StatisticsSerializer(VerboseNameSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop("id", None)  # Remove manually assigned ID

        instance, created = Statistics.objects.get_or_create(
            defaults=validated_data
        )
        if not created:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance
