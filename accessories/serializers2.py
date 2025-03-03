from rest_framework import serializers
from .models import (# 13 * 4 - 2 = 50
    CartonSupplies     , CartonStock     , PackagingCarton     , ReturnCarton,
    HangerSupplies     , HangerStock     , PackagingHanger     , ReturnHanger,
    SizerSupplies      , SizerStock      , PackagingSizer      , ReturnSizer,
    BagSupplies        , BagStock        , PackagingBag        , ReturnBag,
    HangTagSupplies    , HangTagStock    , PackagingHangTag    , ReturnHangTag,
    HeatSealSupplies   , HeatSealStock   , PackagingHeatSeal   , ReturnHeatSeal,
    TicketSatanSupplies, TicketSatanStock, PackagingTicketSatan, ReturnTicketSatan,
    TicketSupplies     , TicketStock     , PackagingTicket     , ReturnTicket,
    TicketPriceSupplies, TicketPriceStock, PackagingTicketPrice, ReturnTicketPrice,
    KardonSupplies     , KardonStock     , PackagingKardon     , ReturnKardon,
    RubberSupplies     , RubberStock     , PackagingRubber     , ReturnRubber,
    ThreadSupplies     , ThreadStock     , PackagingThread     ,
    GlueSupplies       , GlueStock       , PackagingGlue
)


class VerboseNameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) 
    class Meta:
        fields = '__all__'

    def to_representation(self, instance):
        # Convert field names to their verbose_name
        representation = super().to_representation(instance)
        new_representation = {}
        for field_name, value in representation.items():
            model_field = self.Meta.model._meta.get_field(field_name)
            new_representation[model_field.verbose_name] = value
        return new_representation


# Carton Serializers
class CartonSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = CartonSupplies
        fields = '__all__'
        
class CartonStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = CartonStock
        fields = '__all__'
        
class PackagingCartonSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingCarton
        fields = '__all__'
        
class ReturnCartonSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnCarton
        fields = '__all__'
        
# Hanger Serializers
class HangerSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HangerSupplies
        fields = '__all__'
        
class HangerStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HangerStock
        fields = '__all__'
        
class PackagingHangerSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingHanger
        fields = '__all__'
        
class ReturnHangerSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnHanger
        fields = '__all__'
        
# Sizer Serializers
class SizerSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = SizerSupplies
        fields = '__all__'
        
class SizerStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = SizerStock
        fields = '__all__'
        
class PackagingSizerSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingSizer
        fields = '__all__'
        
class ReturnSizerSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnSizer
        fields = '__all__'
        
# Bag Serializers
class BagSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = BagSupplies
        fields = '__all__'
        
class BagStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = BagStock
        fields = '__all__'
        
class PackagingBagSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingBag
        fields = '__all__'
        
class ReturnBagSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnBag
        fields = '__all__'
        
# HangTag Serializers
class HangTagSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HangTagSupplies
        fields = '__all__'
        
class HangTagStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HangTagStock
        fields = '__all__'
        
class PackagingHangTagSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingHangTag
        fields = '__all__'
        
class ReturnHangTagSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnHangTag
        fields = '__all__'
        
# HeatSeal Serializers
class HeatSealSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HeatSealSupplies
        fields = '__all__'
        
class HeatSealStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = HeatSealStock
        fields = '__all__'
        
class PackagingHeatSealSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingHeatSeal
        fields = '__all__'
        
class ReturnHeatSealSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnHeatSeal
        fields = '__all__'
        
# TicketSatan Serializers
class TicketSatanSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketSatanSupplies
        fields = '__all__'
        
class TicketSatanStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketSatanStock
        fields = '__all__'
        
class PackagingTicketSatanSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingTicketSatan
        fields = '__all__'
        
class ReturnTicketSatanSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnTicketSatan
        fields = '__all__'
        
# Ticket Serializers
class TicketSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketSupplies
        fields = '__all__'
        
class TicketStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketStock
        fields = '__all__'
        
class PackagingTicketSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingTicket
        fields = '__all__'
        
class ReturnTicketSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnTicket
        fields = '__all__'
        
# TicketPrice Serializers
class TicketPriceSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketPriceSupplies
        fields = '__all__'
        
class TicketPriceStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = TicketPriceStock
        fields = '__all__'
        
class PackagingTicketPriceSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingTicketPrice
        fields = '__all__'
        
class ReturnTicketPriceSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnTicketPrice
        fields = '__all__'
        
# Kardon Serializers
class KardonSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = KardonSupplies
        fields = '__all__'
        
class KardonStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = KardonStock
        fields = '__all__'
        
class PackagingKardonSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingKardon
        fields = '__all__'
        
class ReturnKardonSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnKardon
        fields = '__all__'
        
# Rubber Serializers
class RubberSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = RubberSupplies
        fields = '__all__'
        
class RubberStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = RubberStock
        fields = '__all__'
        
class PackagingRubberSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingRubber
        fields = '__all__'
        
class ReturnRubberSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ReturnRubber
        fields = '__all__'
        
# Thread Serializers
class ThreadSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ThreadSupplies
        fields = '__all__'
        
class ThreadStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = ThreadStock
        fields = '__all__'
        
class PackagingThreadSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingThread
        fields = '__all__'
        
# Glue Serializers
class GlueSuppliesSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = GlueSupplies
        fields = '__all__'
        
class GlueStockSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = GlueStock
        fields = '__all__'
        
class PackagingGlueSerializer(VerboseNameSerializer):
    class Meta(VerboseNameSerializer.Meta):
        model = PackagingGlue       
        fields = '__all__'
        