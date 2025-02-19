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

class CartonStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CartonStock

class PackagingCartonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingCarton

class ReturnCartonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnCarton

# Hanger Serializers
class HangerSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangerSupplies

class HangerStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangerStock

class PackagingHangerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHanger

class ReturnHangerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHanger

# Sizer Serializers
class SizerSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = SizerSupplies

class SizerStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = SizerStock

class PackagingSizerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingSizer

class ReturnSizerSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnSizer

# Bag Serializers
class BagSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BagSupplies

class BagStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = BagStock

class PackagingBagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingBag

class ReturnBagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnBag

# HangTag Serializers
class HangTagSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangTagSupplies

class HangTagStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HangTagStock

class PackagingHangTagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHangTag

class ReturnHangTagSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHangTag

# HeatSeal Serializers
class HeatSealSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HeatSealSupplies

class HeatSealStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HeatSealStock

class PackagingHeatSealSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingHeatSeal

class ReturnHeatSealSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnHeatSeal

# TicketSatan Serializers
class TicketSatanSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSatanSupplies

class TicketSatanStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSatanStock

class PackagingTicketSatanSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicketSatan

class ReturnTicketSatanSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicketSatan

# Ticket Serializers
class TicketSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketSupplies

class TicketStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketStock

class PackagingTicketSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicket

class ReturnTicketSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicket

# TicketPrice Serializers
class TicketPriceSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketPriceSupplies

class TicketPriceStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = TicketPriceStock

class PackagingTicketPriceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingTicketPrice

class ReturnTicketPriceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnTicketPrice

# Kardon Serializers
class KardonSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = KardonSupplies

class KardonStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = KardonStock

class PackagingKardonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingKardon

class ReturnKardonSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnKardon

# Rubber Serializers
class RubberSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RubberSupplies

class RubberStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RubberStock

class PackagingRubberSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingRubber

class ReturnRubberSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ReturnRubber

# Thread Serializers
class ThreadSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThreadSupplies

class ThreadStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThreadStock

class PackagingThreadSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingThread

# Glue Serializers
class GlueSuppliesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = GlueSupplies

class GlueStockSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = GlueStock

class PackagingGlueSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = PackagingGlue