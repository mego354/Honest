from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny  # Add this import
from cloth.models import Fabric, CutTransfer, ReturnTransfer, Statistics, Updates as Updates1
from cloth.serializers2 import (FabricSerializer, CutTransferSerializer, ReturnTransferSerializer,
                              StatisticsSerializer)
from accessories.models import (CartonSupplies, CartonStock, PackagingCarton, ReturnCarton,
                                HangerSupplies, HangerStock, PackagingHanger, ReturnHanger,
                                SizerSupplies, SizerStock, PackagingSizer, ReturnSizer,
                                BagSupplies, BagStock, PackagingBag, ReturnBag, HangTagSupplies,
                                HangTagStock, PackagingHangTag, ReturnHangTag, HeatSealSupplies,
                                HeatSealStock, PackagingHeatSeal, ReturnHeatSeal, TicketSatanSupplies,
                                TicketSatanStock, PackagingTicketSatan, ReturnTicketSatan, TicketSupplies,
                                TicketStock, PackagingTicket, ReturnTicket, TicketPriceSupplies,
                                TicketPriceStock, PackagingTicketPrice, ReturnTicketPrice,
                                KardonSupplies, KardonStock, PackagingKardon, ReturnKardon,
                                RubberSupplies, RubberStock, PackagingRubber, ReturnRubber,
                                ThreadSupplies, ThreadStock, PackagingThread,
                                GlueSupplies, GlueStock, PackagingGlue)
from accessories.serializers2 import (CartonSuppliesSerializer, CartonStockSerializer, PackagingCartonSerializer, ReturnCartonSerializer,
                                     HangerSuppliesSerializer, HangerStockSerializer, PackagingHangerSerializer, ReturnHangerSerializer,
                                     SizerSuppliesSerializer, SizerStockSerializer, PackagingSizerSerializer, ReturnSizerSerializer,
                                     BagSuppliesSerializer, BagStockSerializer, PackagingBagSerializer, ReturnBagSerializer, HangTagSuppliesSerializer,
                                     HangTagStockSerializer, PackagingHangTagSerializer, ReturnHangTagSerializer, HeatSealSuppliesSerializer,
                                     HeatSealStockSerializer, PackagingHeatSealSerializer, ReturnHeatSealSerializer, TicketSatanSuppliesSerializer,
                                     TicketSatanStockSerializer, PackagingTicketSatanSerializer, ReturnTicketSatanSerializer, TicketSuppliesSerializer,
                                     TicketStockSerializer, PackagingTicketSerializer, ReturnTicketSerializer, TicketPriceSuppliesSerializer,
                                     TicketPriceStockSerializer, PackagingTicketPriceSerializer, ReturnTicketPriceSerializer,
                                     KardonSuppliesSerializer, KardonStockSerializer, PackagingKardonSerializer, ReturnKardonSerializer,
                                     RubberSuppliesSerializer, RubberStockSerializer, PackagingRubberSerializer, ReturnRubberSerializer,
                                     ThreadSuppliesSerializer, ThreadStockSerializer, PackagingThreadSerializer,
                                     GlueSuppliesSerializer, GlueStockSerializer, PackagingGlueSerializer)
from production.models import Model, SizeAmount, Piece, ProductionPiece, Carton, Packing
from production.serializers2 import (ModelSerializer, SizeAmountSerializer, PieceSerializer,
                                    ProductionPieceSerializer, CartonSerializer, PackingSerializer)


class AllDataAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    def get(self, request):
        # Fetch data from cloth
        fabrics = Fabric.objects.all()
        cut_transfers = CutTransfer.objects.all()
        return_transfers = ReturnTransfer.objects.all()
        statistics = Statistics.objects.all()

        # Fetch data from accessories
        carton_supplies = CartonSupplies.objects.all()
        carton_stock = CartonStock.objects.all()
        packaging_carton = PackagingCarton.objects.all()
        return_carton = ReturnCarton.objects.all()
        hanger_supplies = HangerSupplies.objects.all()
        hanger_stock = HangerStock.objects.all()
        packaging_hanger = PackagingHanger.objects.all()
        return_hanger = ReturnHanger.objects.all()
        sizer_supplies = SizerSupplies.objects.all()
        sizer_stock = SizerStock.objects.all()
        packaging_sizer = PackagingSizer.objects.all()
        return_sizer = ReturnSizer.objects.all()
        bag_supplies = BagSupplies.objects.all()
        bag_stock = BagStock.objects.all()
        packaging_bag = PackagingBag.objects.all()
        return_bag = ReturnBag.objects.all()
        hangtag_supplies = HangTagSupplies.objects.all()
        hangtag_stock = HangTagStock.objects.all()
        packaging_hangtag = PackagingHangTag.objects.all()
        return_hangtag = ReturnHangTag.objects.all()
        heatseal_supplies = HeatSealSupplies.objects.all()
        heatseal_stock = HeatSealStock.objects.all()
        packaging_heatseal = PackagingHeatSeal.objects.all()
        return_heatseal = ReturnHeatSeal.objects.all()
        ticketsatan_supplies = TicketSatanSupplies.objects.all()
        ticketsatan_stock = TicketSatanStock.objects.all()
        packaging_ticketsatan = PackagingTicketSatan.objects.all()
        return_ticketsatan = ReturnTicketSatan.objects.all()
        ticket_supplies = TicketSupplies.objects.all()
        ticket_stock = TicketStock.objects.all()
        packaging_ticket = PackagingTicket.objects.all()
        return_ticket = ReturnTicket.objects.all()
        ticketprice_supplies = TicketPriceSupplies.objects.all()
        ticketprice_stock = TicketPriceStock.objects.all()
        packaging_ticketprice = PackagingTicketPrice.objects.all()
        return_ticketprice = ReturnTicketPrice.objects.all()
        kardon_supplies = KardonSupplies.objects.all()
        kardon_stock = KardonStock.objects.all()
        packaging_kardon = PackagingKardon.objects.all()
        return_kardon = ReturnKardon.objects.all()
        rubber_supplies = RubberSupplies.objects.all()
        rubber_stock = RubberStock.objects.all()
        packaging_rubber = PackagingRubber.objects.all()
        return_rubber = ReturnRubber.objects.all()
        thread_supplies = ThreadSupplies.objects.all()
        thread_stock = ThreadStock.objects.all()
        packaging_thread = PackagingThread.objects.all()
        glue_supplies = GlueSupplies.objects.all()
        glue_stock = GlueStock.objects.all()
        packaging_glue = PackagingGlue.objects.all()

        # Fetch data from production
        models = Model.objects.all()
        size_amounts = SizeAmount.objects.all()
        pieces = Piece.objects.all()
        production_pieces = ProductionPiece.objects.all()
        cartons = Carton.objects.all()
        packings = Packing.objects.all()

        # Serialize data with Arabic labels
        data = {
            "الأقمشة": {  # cloth app
                "القماش": FabricSerializer(fabrics, many=True).data,
                "قص القماش": CutTransferSerializer(cut_transfers, many=True).data,
                "مرتجعات القماش": ReturnTransferSerializer(return_transfers, many=True).data,
                "الإحصائيات العمليات": StatisticsSerializer(statistics, many=True).data,
            },
            "الإكسسوارات": {  # accessories app
                "إمدادات الكراتين": CartonSuppliesSerializer(carton_supplies, many=True).data,
                "مخزون الكراتين": CartonStockSerializer(carton_stock, many=True).data,
                "تعبئة الكراتين": PackagingCartonSerializer(packaging_carton, many=True).data,
                "مرتجعات الكراتين": ReturnCartonSerializer(return_carton, many=True).data,
                "إمدادات الشماعات": HangerSuppliesSerializer(hanger_supplies, many=True).data,
                "مخزون الشماعات": HangerStockSerializer(hanger_stock, many=True).data,
                "تعبئة الشماعات": PackagingHangerSerializer(packaging_hanger, many=True).data,
                "مرتجعات الشماعات": ReturnHangerSerializer(return_hanger, many=True).data,
                "إمدادات السيزر": SizerSuppliesSerializer(sizer_supplies, many=True).data,
                "مخزون السيزر": SizerStockSerializer(sizer_stock, many=True).data,
                "تعبئة السيزر": PackagingSizerSerializer(packaging_sizer, many=True).data,
                "مرتجعات السيزر": ReturnSizerSerializer(return_sizer, many=True).data,
                "إمدادات الأكياس": BagSuppliesSerializer(bag_supplies, many=True).data,
                "مخزون الأكياس": BagStockSerializer(bag_stock, many=True).data,
                "تعبئة الأكياس": PackagingBagSerializer(packaging_bag, many=True).data,
                "مرتجعات الأكياس": ReturnBagSerializer(return_bag, many=True).data,
                "إمدادات الهانج تاج": HangTagSuppliesSerializer(hangtag_supplies, many=True).data,
                "مخزون الهانج تاج": HangTagStockSerializer(hangtag_stock, many=True).data,
                "تعبئة الهانج تاج": PackagingHangTagSerializer(packaging_hangtag, many=True).data,
                "مرتجعات الهانج تاج": ReturnHangTagSerializer(return_hangtag, many=True).data,
                "إمدادات الهيت سيل": HeatSealSuppliesSerializer(heatseal_supplies, many=True).data,
                "مخزون الهيت سيل": HeatSealStockSerializer(heatseal_stock, many=True).data,
                "تعبئة الهيت سيل": PackagingHeatSealSerializer(packaging_heatseal, many=True).data,
                "مرتجعات الهيت سيل": ReturnHeatSealSerializer(return_heatseal, many=True).data,
                "إمدادات تيكت ساتان": TicketSatanSuppliesSerializer(ticketsatan_supplies, many=True).data,
                "مخزون تيكت ساتان": TicketSatanStockSerializer(ticketsatan_stock, many=True).data,
                "تعبئة تيكت ساتان": PackagingTicketSatanSerializer(packaging_ticketsatan, many=True).data,
                "مرتجعات تيكت ساتان": ReturnTicketSatanSerializer(return_ticketsatan, many=True).data,
                "إمدادات التيكت الرئيسي": TicketSuppliesSerializer(ticket_supplies, many=True).data,
                "مخزون التيكت الرئيسي": TicketStockSerializer(ticket_stock, many=True).data,
                "تعبئة التيكت الرئيسي": PackagingTicketSerializer(packaging_ticket, many=True).data,
                "مرتجعات التيكت الرئيسي": ReturnTicketSerializer(return_ticket, many=True).data,
                "إمدادات تيكت برايس": TicketPriceSuppliesSerializer(ticketprice_supplies, many=True).data,
                "مخزون تيكت برايس": TicketPriceStockSerializer(ticketprice_stock, many=True).data,
                "تعبئة تيكت برايس": PackagingTicketPriceSerializer(packaging_ticketprice, many=True).data,
                "مرتجعات تيكت برايس": ReturnTicketPriceSerializer(return_ticketprice, many=True).data,
                "إمدادات الكردون": KardonSuppliesSerializer(kardon_supplies, many=True).data,
                "مخزون الكردون": KardonStockSerializer(kardon_stock, many=True).data,
                "تعبئة الكردون": PackagingKardonSerializer(packaging_kardon, many=True).data,
                "مرتجعات الكردون": ReturnKardonSerializer(return_kardon, many=True).data,
                "إمدادات اللزق": RubberSuppliesSerializer(rubber_supplies, many=True).data,
                "مخزون اللزق": RubberStockSerializer(rubber_stock, many=True).data,
                "تعبئة اللزق": PackagingRubberSerializer(packaging_rubber, many=True).data,
                "مرتجعات اللزق": ReturnRubberSerializer(return_rubber, many=True).data,
                "إمدادات الخيوط": ThreadSuppliesSerializer(thread_supplies, many=True).data,
                "مخزون الخيوط": ThreadStockSerializer(thread_stock, many=True).data,
                "تعبئة الخيوط": PackagingThreadSerializer(packaging_thread, many=True).data,
                "إمدادات اللزق": GlueSuppliesSerializer(glue_supplies, many=True).data,
                "مخزون اللزق": GlueStockSerializer(glue_stock, many=True).data,
                "تعبئة اللزق": PackagingGlueSerializer(packaging_glue, many=True).data,
            },
            "الإنتاج": {  # production app
                "الموديلات": ModelSerializer(models, many=True).data,
                "كميات المقاسات": SizeAmountSerializer(size_amounts, many=True).data,
                "القطع": PieceSerializer(pieces, many=True).data,
                "قطع الإنتاج": ProductionPieceSerializer(production_pieces, many=True).data,
                "الكراتين": CartonSerializer(cartons, many=True).data,
                "التعبئة": PackingSerializer(packings, many=True).data,
            }
        }

        return Response(data)