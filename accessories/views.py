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
    columns = ["التاريخ","اسم المورد","رقم الموديل","المقاس","عدد الربط","الكمية في الربطة","الفرط","العدد الإجمالي"]


class CartonStockView(FilterableListView):
    template_name = "accessories/CartonStock.html"
    model = CartonStock
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["رقم الموديل","المقاس","العدد الإجمالي"]


class PackagingCartonView(FilterableListView):
    template_name = "accessories/PackagingCarton.html"
    model = PackagingCarton
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["التاريخ","رقم الموديل","المقاس","عدد الكرتون","المصنع"]


class ReturnCartonView(FilterableListView):
    template_name = "accessories/ReturnCarton.html"
    model = ReturnCarton
    filter_fields = ['model_number', 'length', 'width', 'height']
    columns = ["التاريخ","رقم الموديل","المقاس","عدد الكرتون","العدد الإجمالي"]

###############################################################################################################################
class HangerSuppliesView(FilterableListView):
    template_name = "accessories/HangerSupplies.html"
    model = HangerSupplies
    filter_fields = ['hanger_number', 'color']
    columns = ["رقم الشماعة","اللون","عدد الدست","عدد الشماعات","اسم المورد","التاريخ"]

class HangerStockView(FilterableListView):
    template_name = "accessories/HangerStock.html"
    model = HangerStock
    filter_fields = ['hanger_number', 'color']
    columns = ["رقم الشماعة","اللون","عدد الدست","عدد الشماعات",]


class PackagingHangerView(FilterableListView):
    template_name = "accessories/PackagingHanger.html"
    model = PackagingHanger
    filter_fields = ['hanger_number', 'color']
    columns = ["رقم الشماعة","اللون","عدد الدست","عدد الشماعات","اسم المصنع","التاريخ"]


class ReturnHangerView(FilterableListView):
    template_name = "accessories/ReturnHanger.html"
    model = ReturnHanger
    filter_fields = ['hanger_number', 'color']
    columns = ["رقم الشماعة","اللون","عدد الدست","عدد الشماعات","التاريخ"]

###############################################################################################################################
class SizerSuppliesView(FilterableListView):
    template_name = "accessories/SizerSupplies.html"
    model = SizerSupplies
    filter_fields = ['size', 'color']
    columns = ["المقاس","اللون","عدد السيزر","اسم المورد","التاريخ"]

class SizerStockView(FilterableListView):
    template_name = "accessories/SizerStock.html"
    model = SizerStock
    filter_fields = ['size', 'color']
    columns = ["المقاس","اللون","عدد السيزر"]

class PackagingSizerView(FilterableListView):
    template_name = "accessories/PackagingSizer.html"
    model = PackagingSizer
    filter_fields = ['size', 'color']
    columns = ["المقاس","اللون","عدد السيزر","المصنع","التاريخ"]

class ReturnSizerView(FilterableListView):
    template_name = "accessories/ReturnSizer.html"
    model = ReturnSizer
    filter_fields = ['size', 'color']
    columns = ["المقاس","اللون","عدد السيزر","التاريخ"]

###############################################################################################################################
class BagSuppliesView(FilterableListView):
    template_name = "accessories/BagSupplies.html"
    model = BagSupplies
    filter_fields = ['bag_length', 'bag_width', 'weight']
    columns = ["الطول","العرض","الوزن","الاكياس في الكيلو","عدد الاكياس","اسم المورد","التاريخ"]


class BagStockView(FilterableListView):
    template_name = "accessories/BagStock.html"
    model = BagStock
    filter_fields = ['bag_length', 'bag_width', 'weight']
    columns = ["الطول","العرض","الوزن","الاكياس في الكيلو","عدد الاكياس"]

class PackagingBagView(FilterableListView):
    template_name = "accessories/PackagingBag.html"
    model = PackagingBag
    filter_fields = ['bag_length', 'bag_width', 'weight']
    columns = ["الطول","العرض","الوزن","الاكياس في الكيلو","عدد الاكياس","المصنع","التاريخ"]

class ReturnBagView(FilterableListView):
    template_name = "accessories/ReturnBag.html"
    model = ReturnBag
    filter_fields = ['bag_length', 'bag_width', 'weight']
    columns = ["الطول","العرض","الوزن","الاكياس في الكيلو","عدد الاكياس","التاريخ"]

###############################################################################################################################
class HangTagSuppliesView(FilterableListView):
    template_name = "accessories/HangTagSupplies.html"
    model = HangTagSupplies
    filter_fields = ['type']
    columns = ["النوع","العدد","اسم المورد","التاريخ"]

class HangTagStockView(FilterableListView):
    template_name = "accessories/HangTagStock.html"
    model = HangTagStock
    filter_fields = ['type']
    columns = ["النوع","العدد",]

class PackagingHangTagView(FilterableListView):
    template_name = "accessories/PackagingHangTag.html"
    model = PackagingHangTag
    filter_fields = ['type']
    columns = ["النوع","العدد","المصنع","التاريخ"]

class ReturnHangTagView(FilterableListView):
    template_name = "accessories/ReturnHangTag.html"
    model = ReturnHangTag
    filter_fields = ['type']
    columns = ["النوع","العدد","التاريخ"]

###############################################################################################################################
class HeatSealSuppliesView(FilterableListView):
    template_name = "accessories/HeatSealSupplies.html"
    model = HeatSealSupplies
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","العدد","اسم المورد","التاريخ"]

class HeatSealStockView(FilterableListView):
    template_name = "accessories/HeatSealStock.html"
    model = HeatSealStock
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","العدد","اسم المورد"]

class PackagingHeatSealView(FilterableListView):
    template_name = "accessories/PackagingHeatSeal.html"
    model = PackagingHeatSeal
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","العدد","اسم المصنع","التاريخ"]

class ReturnHeatSealView(FilterableListView):
    template_name = "accessories/ReturnHeatSeal.html"
    model = ReturnHeatSeal
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","العدد","التاريخ"]

###############################################################################################################################
class TicketSatanSuppliesView(FilterableListView):
    template_name = "accessories/TicketSatanSupplies.html"
    model = TicketSatanSupplies
    filter_fields = ['model_number', 'size', 'upc_number']
    columns = ["رقم الموديل","المقاس","نسبة القطن","نسبة البوليستر","UPC Number","عدد القطع","اسم المورد","التاريخ"]

class TicketSatanStockView(FilterableListView):
    template_name = "accessories/TicketSatanStock.html"
    model = TicketSatanStock
    filter_fields = ['model_number', 'size', 'upc_number']
    columns = ["رقم الموديل","المقاس","نسبة القطن","نسبة البوليستر","UPC Number","عدد القطع"]

class PackagingTicketSatanView(FilterableListView):
    template_name = "accessories/PackagingTicketSatan.html"
    model = PackagingTicketSatan
    filter_fields = ['model_number', 'size', 'upc_number']
    columns = ["رقم الموديل","المقاس","نسبة القطن","نسبة البوليستر","UPC Number","عدد القطع","اسم المصنع","التاريخ"]

class ReturnTicketSatanView(FilterableListView):
    template_name = "accessories/ReturnTicketSatan.html"
    model = ReturnTicketSatan
    filter_fields = ['model_number', 'size', 'upc_number']
    columns = ["رقم الموديل","المقاس","نسبة القطن","نسبة البوليستر","UPC Number","عدد القطع","التاريخ"]

###############################################################################################################################
class TicketSuppliesView(FilterableListView):
    template_name = "accessories/TicketSupplies.html"
    model = TicketSupplies
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","عدد القطع","اسم المورد","التاريخ"]

class TicketStockView(FilterableListView):
    template_name = "accessories/TicketStock.html"
    model = TicketStock
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","عدد القطع"]

class PackagingTicketView(FilterableListView):
    template_name = "accessories/PackagingTicket.html"
    model = PackagingTicket
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","عدد القطع","اسم المصنع","التاريخ"]

class ReturnTicketView(FilterableListView):
    template_name = "accessories/ReturnTicket.html"
    model = ReturnTicket
    filter_fields = ['type', 'size']
    columns = ["النوع","المقاس","عدد القطع","التاريخ"]

###############################################################################################################################
class TicketPriceSuppliesView(FilterableListView):
    template_name = "accessories/TicketPriceSupplies.html"
    model = TicketPriceSupplies
    filter_fields = ['model_number', 'size']
    columns = ["الاجمالي","المقاس","رقم الموديل","اسم المورد","التاريخ"]

class TicketPriceStockView(FilterableListView):
    template_name = "accessories/TicketPriceStock.html"
    model = TicketPriceStock
    filter_fields = ['model_number', 'size']
    columns = ["الاجمالي","المقاس","رقم الموديل"]

class PackagingTicketPriceView(FilterableListView):
    template_name = "accessories/PackagingTicketPrice.html"
    model = PackagingTicketPrice
    filter_fields = ['model_number', 'size']
    columns = ["الاجمالي","المقاس","رقم الموديل","اسم المصنع","التاريخ"]

class ReturnTicketPriceView(FilterableListView):
    template_name = "accessories/ReturnTicketPrice.html"
    model = ReturnTicketPrice
    filter_fields = ['model_number', 'size']
    columns = ["الاجمالي","المقاس","رقم الموديل","التاريخ"]

###############################################################################################################################
class KardonSuppliesView(FilterableListView):
    template_name = "accessories/KardonSupplies.html"
    model = KardonSupplies
    filter_fields = ['color']
    columns = ["عدد الامتار","اللون","اسم المورد","التاريخ"]

class KardonStockView(FilterableListView):
    template_name = "accessories/KardonStock.html"
    model = KardonStock
    filter_fields = ['color']
    columns = ["عدد الامتار","اللون"]

class PackagingKardonView(FilterableListView):
    template_name = "accessories/PackagingKardon.html"
    model = PackagingKardon
    filter_fields = ['color']
    columns = ["عدد الامتار","اللون","اسم المصنع","التاريخ"]

class ReturnKardonView(FilterableListView):
    template_name = "accessories/ReturnKardon.html"
    model = ReturnKardon
    filter_fields = ['color']
    columns = ["عدد الامتار","اللون","التاريخ"]

###############################################################################################################################
class RubberSuppliesView(FilterableListView):
    template_name = "accessories/RubberSupplies.html"
    model = RubberSupplies
    filter_fields = ['width']
    columns = ["الوزن الاجمالي","عرض الاستك","اسم المورد","التاريخ"]

class RubberStockView(FilterableListView):
    template_name = "accessories/RubberStock.html"
    model = RubberStock
    filter_fields = ['width']
    columns = ["الوزن الاجمالي","عرض الاستك","اسم المورد"]

class PackagingRubberView(FilterableListView):
    template_name = "accessories/PackagingRubber.html"
    model = PackagingRubber
    filter_fields = ['width']
    columns = ["الوزن الاجمالي","عرض الاستك","اسم المصنع","التاريخ"]

class ReturnRubberView(FilterableListView):
    template_name = "accessories/ReturnRubber.html"
    model = ReturnRubber
    filter_fields = ['width']
    columns = ["الوزن الاجمالي","عرض الاستك","التاريخ"]

###############################################################################################################################
class ThreadSuppliesView(FilterableListView):
    template_name = "accessories/ThreadSupplies.html"
    model = ThreadSupplies
    filter_fields = ['thread_code', 'color']
    columns = ["عدد البكر","اللون","كود الخيط","اسم المورد","التاريخ"]

class ThreadStockView(FilterableListView):
    template_name = "accessories/ThreadStock.html"
    model = ThreadStock
    filter_fields = ['thread_code', 'color']
    columns = ["عدد البكر","اللون","كود الخيط"]


class PackagingThreadView(FilterableListView):
    template_name = "accessories/PackagingThread.html"
    model = PackagingThread
    filter_fields = ['thread_code', 'color']
    columns = ["عدد البكر","اللون","كود الخيط","اسم المصنع","التاريخ"]

###############################################################################################################################
class GlueSuppliesView(FilterableListView):
    template_name = "accessories/GlueSupplies.html"
    model = GlueSupplies
    filter_fields = ['width']
    columns = ["عدد الكراتين","عرض اللزق","اسم المورد","التاريخ"]


class GlueStockView(FilterableListView):
    template_name = "accessories/GlueStock.html"
    model = GlueStock
    filter_fields = ['width']
    columns = ["عدد الكراتين","عرض اللزق","اسم المورد"]

class PackagingGlueView(FilterableListView):
    template_name = "accessories/PackagingGlue.html"
    model = PackagingGlue
    filter_fields = ['width']
    columns = ["عدد الكراتين","عرض اللزق","اسم المصنع","التاريخ"]

###############################################################################################################################
