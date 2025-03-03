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

# Base Serializer (Optional, for reusability)
class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) 

    class Meta:
        fields = '__all__'

# Carton Serializers
class CartonSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CartonSupplies
        fields = '__all__'
        
class CartonStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CartonStock
        fields = '__all__'
        
class PackagingCartonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingCarton
        fields = '__all__'
        
class ReturnCartonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnCarton
        fields = '__all__'
        
# Hanger Serializers
class HangerSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangerSupplies
        fields = '__all__'
        
class HangerStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangerStock
        fields = '__all__'
        
class PackagingHangerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHanger
        fields = '__all__'
        
class ReturnHangerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHanger
        fields = '__all__'
        
# Sizer Serializers
class SizerSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = SizerSupplies
        fields = '__all__'
        
class SizerStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = SizerStock
        fields = '__all__'
        
class PackagingSizerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingSizer
        fields = '__all__'
        
class ReturnSizerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnSizer
        fields = '__all__'
        
# Bag Serializers
class BagSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BagSupplies
        fields = '__all__'
        
class BagStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BagStock
        fields = '__all__'
        
class PackagingBagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingBag
        fields = '__all__'
        
class ReturnBagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnBag
        fields = '__all__'
        
# HangTag Serializers
class HangTagSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangTagSupplies
        fields = '__all__'
        
class HangTagStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangTagStock
        fields = '__all__'
        
class PackagingHangTagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHangTag
        fields = '__all__'
        
class ReturnHangTagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHangTag
        fields = '__all__'
        
# HeatSeal Serializers
class HeatSealSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HeatSealSupplies
        fields = '__all__'
        
class HeatSealStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HeatSealStock
        fields = '__all__'
        
class PackagingHeatSealSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHeatSeal
        fields = '__all__'
        
class ReturnHeatSealSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHeatSeal
        fields = '__all__'
        
# TicketSatan Serializers
class TicketSatanSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSatanSupplies
        fields = '__all__'
        
class TicketSatanStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSatanStock
        fields = '__all__'
        
class PackagingTicketSatanSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicketSatan
        fields = '__all__'
        
class ReturnTicketSatanSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicketSatan
        fields = '__all__'
        
# Ticket Serializers
class TicketSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSupplies
        fields = '__all__'
        
class TicketStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketStock
        fields = '__all__'
        
class PackagingTicketSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicket
        fields = '__all__'
        
class ReturnTicketSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicket
        fields = '__all__'
        
# TicketPrice Serializers
class TicketPriceSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketPriceSupplies
        fields = '__all__'
        
class TicketPriceStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketPriceStock
        fields = '__all__'
        
class PackagingTicketPriceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicketPrice
        fields = '__all__'
        
class ReturnTicketPriceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicketPrice
        fields = '__all__'
        
# Kardon Serializers
class KardonSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = KardonSupplies
        fields = '__all__'
        
class KardonStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = KardonStock
        fields = '__all__'
        
class PackagingKardonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingKardon
        fields = '__all__'
        
class ReturnKardonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnKardon
        fields = '__all__'
        
# Rubber Serializers
class RubberSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RubberSupplies
        fields = '__all__'
        
class RubberStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RubberStock
        fields = '__all__'
        
class PackagingRubberSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingRubber
        fields = '__all__'
        
class ReturnRubberSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnRubber
        fields = '__all__'
        
# Thread Serializers
class ThreadSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThreadSupplies
        fields = '__all__'
        
class ThreadStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThreadStock
        fields = '__all__'
        
class PackagingThreadSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingThread
        fields = '__all__'
        
# Glue Serializers
class GlueSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = GlueSupplies
        fields = '__all__'
        
class GlueStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = GlueStock
        fields = '__all__'
        
class PackagingGlueSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingGlue       
        fields = '__all__'
        