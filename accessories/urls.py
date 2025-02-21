from django.urls import path
from .views import *
from .api import PopulateModelsView


urlpatterns = [
    path('', CartonSuppliesView.as_view(), name='CartonSuppliesView'),
    path('CartonSupplies/', CartonSuppliesView.as_view(), name='CartonSuppliesView'),
    path('CartonStock/', CartonStockView.as_view(), name='CartonStockView'),
    path('PackagingCarton/', PackagingCartonView.as_view(), name='PackagingCartonView'),
    path('ReturnCartontics/', ReturnCartonView.as_view(), name='ReturnCartonView'),
    path('HangerSuppliestics/', HangerSuppliesView.as_view(), name='HangerSuppliesView'),
    path('HangerStock/', HangerStockView.as_view(), name='HangerStockView'),
    path('PackagingHanger/', PackagingHangerView.as_view(), name='PackagingHangerView'),
    path('ReturnHanger/', ReturnHangerView.as_view(), name='ReturnHangerView'),
    path('SizerSuppliestics/', SizerSuppliesView.as_view(), name='SizerSuppliesView'),
    path('SizerStocktics/', SizerStockView.as_view(), name='SizerStockView'),
    path('PackagingSizer/', PackagingSizerView.as_view(), name='PackagingSizerView'),
    path('ReturnSizer/', ReturnSizerView.as_view(), name='ReturnSizerView'),
    path('BagSupplies/', BagSuppliesView.as_view(), name='BagSuppliesView'),
    path('BagStocktics/', BagStockView.as_view(), name='BagStockView'),
    path('PackagingBagtics/', PackagingBagView.as_view(), name='PackagingBagView'),
    path('ReturnBag/', ReturnBagView.as_view(), name='ReturnBagView'),
    path('HangTagSupplies/', HangTagSuppliesView.as_view(), name='HangTagSuppliesView'),
    path('HangTagStock/', HangTagStockView.as_view(), name='HangTagStockView'),
    path('PackagingHangTagtics/', PackagingHangTagView.as_view(), name='PackagingHangTagView'),
    path('ReturnHangTagtics/', ReturnHangTagView.as_view(), name='ReturnHangTagView'),
    path('HeatSealSupplies/', HeatSealSuppliesView.as_view(), name='HeatSealSuppliesView'),
    path('HeatSealStock/', HeatSealStockView.as_view(), name='HeatSealStockView'),
    path('PackagingHeatSeal/', PackagingHeatSealView.as_view(), name='PackagingHeatSealView'),
    path('ReturnHeatSealtics/', ReturnHeatSealView.as_view(), name='ReturnHeatSealView'),
    path('TicketSatanSuppliestics/', TicketSatanSuppliesView.as_view(), name='TicketSatanSuppliesView'),
    path('TicketSatanStock/', TicketSatanStockView.as_view(), name='TicketSatanStockView'),
    path('PackagingTicketSatan/', PackagingTicketSatanView.as_view(), name='PackagingTicketSatanView'),
    path('ReturnTicketSatan/', ReturnTicketSatanView.as_view(), name='ReturnTicketSatanView'),
    path('TicketSuppliestics/', TicketSuppliesView.as_view(), name='TicketSuppliesView'),
    path('TicketStocktics/', TicketStockView.as_view(), name='TicketStockView'),
    path('PackagingTicket/', PackagingTicketView.as_view(), name='PackagingTicketView'),
    path('ReturnTicket/', ReturnTicketView.as_view(), name='ReturnTicketView'),
    path('TicketPriceSupplies/', TicketPriceSuppliesView.as_view(), name='TicketPriceSuppliesView'),
    path('TicketPriceStocktics/', TicketPriceStockView.as_view(), name='TicketPriceStockView'),
    path('PackagingTicketPricetics/', PackagingTicketPriceView.as_view(), name='PackagingTicketPriceView'),
    path('ReturnTicketPrice/', ReturnTicketPriceView.as_view(), name='ReturnTicketPriceView'),
    path('KardonSupplies/', KardonSuppliesView.as_view(), name='KardonSuppliesView'),
    path('KardonStock/', KardonStockView.as_view(), name='KardonStockView'),
    path('PackagingKardontics/', PackagingKardonView.as_view(), name='PackagingKardonView'),
    path('ReturnKardontics/', ReturnKardonView.as_view(), name='ReturnKardonView'),
    path('RubberSupplies/', RubberSuppliesView.as_view(), name='RubberSuppliesView'),
    path('RubberStock/', RubberStockView.as_view(), name='RubberStockView'),
    path('PackagingRubber/', PackagingRubberView.as_view(), name='PackagingRubberView'),
    path('ReturnRubbertics/', ReturnRubberView.as_view(), name='ReturnRubberView'),
    path('ThreadSuppliestics/', ThreadSuppliesView.as_view(), name='ThreadSuppliesView'),
    path('ThreadStock/', ThreadStockView.as_view(), name='ThreadStockView'),
    path('PackagingThread/', PackagingThreadView.as_view(), name='PackagingThreadView'),
    path('GlueSupplies/', GlueSuppliesView.as_view(), name='GlueSuppliesView'),
    path('GlueStocktics/', GlueStockView.as_view(), name='GlueStockView'),
    path('PackagingGluetics/', PackagingGlueView.as_view(), name='PackagingGlueView'),

    path('api/populate-models/', PopulateModelsView.as_view(), name='populate-models'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
]
