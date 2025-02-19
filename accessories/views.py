from django.views.generic import ListView
from django.db.models import Q
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
    ThreadSupplies     , ThreadStock     , PackagingThread     , Updates,
    GlueSupplies       , GlueStock       , PackagingGlue       ,
)

from django.utils.timezone import localtime
from datetime import datetime

import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cloth.PDF import PDFTableGenerator

@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        try:
            # Parse the request data
            request_data = json.loads(request.body)
            data = request_data.get('data', [])
            columns = request_data.get('columns', [])
            footer = request_data.get('footer', "")
            
            # Generate the PDF
            pdf_generator = PDFTableGenerator(data, columns, footer)
            pdf_path = pdf_generator.generate_pdf()  # Returns the file path
            
            # Read the generated PDF file
            with open(pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Create the response
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="fabric_record.pdf"'
            return response

        except Exception as e:
            # Handle exceptions and return an error response
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)

###############################################################################################################################

class FilterableListView(ListView):
    template_name = None
    model = None
    columns = None
    filter_fields = []  # To be defined in the child views
    context_object_name = 'models'


    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        # Apply filters dynamically
        for field in self.filter_fields:
            filter_value = self.request.GET.get(field)
            if filter_value:
                filters &= Q(**{f"{field}__icontains": filter_value})

        # Apply the filters
        filtered_queryset = queryset.filter(filters)
        try:
            filtered_queryset = filtered_queryset.order_by('-date')
        except:
            pass


        return filtered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Format the date in the desired string format
        update = Updates.objects.all().order_by('-date').first()
        context['update'] = localtime(update.date).strftime("%d/%m %I:%M %p") if update and update.date else None
        context['columns'] = self.columns

        # Retrieve verbose names for the filter fields dynamically
        model_meta = self.model._meta
        context['filter_fields'] = [
            {
                'field_name': field,
                'verbose_name': model_meta.get_field(field).verbose_name,
                'value': self.request.GET.get(field) or "",
            }
            for field in self.filter_fields
        ]

        return context

###############################################################################################################################
class CartonSuppliesView(FilterableListView):
    template_name = "accessories/CartonSupplies.html"
    model = CartonSupplies
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["التاريخ","اسم المورد","رقم الموديل","المقاس (الطول)","المقاس (العرض)","المقاس (الارتفاع)","العدد الإجمالي","عدد الربط","الكمية في الربطة","الفرط","العدد الإجمالي"]


class CartonStockView(FilterableListView):
    template_name = "accessories/CartonStock.html"
    model = CartonStock
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["رقم الموديل","المقاس (الطول)","المقاس (العرض)","المقاس (الارتفاع)","العدد الإجمالي"]


class PackagingCartonView(FilterableListView):
    template_name = "accessories/PackagingCarton.html"
    model = PackagingCarton
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["التاريخ","رقم الموديل","المقاس (الطول)","المقاس (العرض)","المقاس (الارتفاع)","عدد الكرتون","المصنع"]


class ReturnCartonView(FilterableListView):
    template_name = "accessories/ReturnCarton.html"
    model = ReturnCarton
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["التاريخ","رقم الموديل","المقاس (الطول)","المقاس (العرض)","المقاس (الارتفاع)","عدد الكرتون","العدد الإجمالي"]

class HangerSuppliesView(FilterableListView):
    template_name = "accessories/HangerSupplies.html"
    model = HangerSupplies
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class HangerStockView(FilterableListView):
    template_name = "accessories/HangerStock.html"
    model = HangerStock
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingHangerView(FilterableListView):
    template_name = "accessories/PackagingHanger.html"
    model = PackagingHanger
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnHangerView(FilterableListView):
    template_name = "accessories/ReturnHanger.html"
    model = ReturnHanger
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class SizerSuppliesView(FilterableListView):
    template_name = "accessories/SizerSupplies.html"
    model = SizerSupplies
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class SizerStockView(FilterableListView):
    template_name = "accessories/SizerStock.html"
    model = SizerStock
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class PackagingSizerView(FilterableListView):
    template_name = "accessories/PackagingSizer.html"
    model = PackagingSizer
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnSizerView(FilterableListView):
    template_name = "accessories/ReturnSizer.html"
    model = ReturnSizer
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class BagSuppliesView(FilterableListView):
    template_name = "accessories/BagSupplies.html"
    model = BagSupplies
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class BagStockView(FilterableListView):
    template_name = "accessories/BagStock.html"
    model = BagStock
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class PackagingBagView(FilterableListView):
    template_name = "accessories/PackagingBag.html"
    model = PackagingBag
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ReturnBagView(FilterableListView):
    template_name = "accessories/ReturnBag.html"
    model = ReturnBag
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class HangTagSuppliesView(FilterableListView):
    template_name = "accessories/HangTagSupplies.html"
    model = HangTagSupplies
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class HangTagStockView(FilterableListView):
    template_name = "accessories/HangTagStock.html"
    model = HangTagStock
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingHangTagView(FilterableListView):
    template_name = "accessories/PackagingHangTag.html"
    model = PackagingHangTag
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ReturnHangTagView(FilterableListView):
    template_name = "accessories/ReturnHangTag.html"
    model = ReturnHangTag
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class HeatSealSuppliesView(FilterableListView):
    template_name = "accessories/HeatSealSupplies.html"
    model = HeatSealSupplies
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class HeatSealStockView(FilterableListView):
    template_name = "accessories/HeatSealStock.html"
    model = HeatSealStock
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingHeatSealView(FilterableListView):
    template_name = "accessories/PackagingHeatSeal.html"
    model = PackagingHeatSeal
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnHeatSealView(FilterableListView):
    template_name = "accessories/ReturnHeatSeal.html"
    model = ReturnHeatSeal
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class TicketSatanSuppliesView(FilterableListView):
    template_name = "accessories/TicketSatanSupplies.html"
    model = TicketSatanSupplies
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class TicketSatanStockView(FilterableListView):
    template_name = "accessories/TicketSatanStock.html"
    model = TicketSatanStock
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingTicketSatanView(FilterableListView):
    template_name = "accessories/PackagingTicketSatan.html"
    model = PackagingTicketSatan
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnTicketSatanView(FilterableListView):
    template_name = "accessories/ReturnTicketSatan.html"
    model = ReturnTicketSatan
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class TicketSuppliesView(FilterableListView):
    template_name = "accessories/TicketSupplies.html"
    model = TicketSupplies
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class TicketStockView(FilterableListView):
    template_name = "accessories/TicketStock.html"
    model = TicketStock
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class PackagingTicketView(FilterableListView):
    template_name = "accessories/PackagingTicket.html"
    model = PackagingTicket
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnTicketView(FilterableListView):
    template_name = "accessories/ReturnTicket.html"
    model = ReturnTicket
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class TicketPriceSuppliesView(FilterableListView):
    template_name = "accessories/TicketPriceSupplies.html"
    model = TicketPriceSupplies
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class TicketPriceStockView(FilterableListView):
    template_name = "accessories/TicketPriceStock.html"
    model = TicketPriceStock
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class PackagingTicketPriceView(FilterableListView):
    template_name = "accessories/PackagingTicketPrice.html"
    model = PackagingTicketPrice
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ReturnTicketPriceView(FilterableListView):
    template_name = "accessories/ReturnTicketPrice.html"
    model = ReturnTicketPrice
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class KardonSuppliesView(FilterableListView):
    template_name = "accessories/KardonSupplies.html"
    model = KardonSupplies
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class KardonStockView(FilterableListView):
    template_name = "accessories/KardonStock.html"
    model = KardonStock
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingKardonView(FilterableListView):
    template_name = "accessories/PackagingKardon.html"
    model = PackagingKardon
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ReturnKardonView(FilterableListView):
    template_name = "accessories/ReturnKardon.html"
    model = ReturnKardon
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class RubberSuppliesView(FilterableListView):
    template_name = "accessories/RubberSupplies.html"
    model = RubberSupplies
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class RubberStockView(FilterableListView):
    template_name = "accessories/RubberStock.html"
    model = RubberStock
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingRubberView(FilterableListView):
    template_name = "accessories/PackagingRubber.html"
    model = PackagingRubber
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class ReturnRubberView(FilterableListView):
    template_name = "accessories/ReturnRubber.html"
    model = ReturnRubber
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ThreadSuppliesView(FilterableListView):
    template_name = "accessories/ThreadSupplies.html"
    model = ThreadSupplies
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class ThreadStockView(FilterableListView):
    template_name = "accessories/ThreadStock.html"
    model = ThreadStock
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class PackagingThreadView(FilterableListView):
    template_name = "accessories/PackagingThread.html"
    model = PackagingThread
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class GlueSuppliesView(FilterableListView):
    template_name = "accessories/GlueSupplies.html"
    model = GlueSupplies
    filter_fields = ['fabric_code', 'model_number']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]


class GlueStockView(FilterableListView):
    template_name = "accessories/GlueStock.html"
    model = GlueStock
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

class PackagingGlueView(FilterableListView):
    template_name = "accessories/PackagingGlue.html"
    model = PackagingGlue
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","اللون","اللون","اللون","اللون","الوزن","المصبغة"]

###############################################################################################################################
