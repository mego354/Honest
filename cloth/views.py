from ast import Return
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics, Updates

from django.utils.timezone import localtime
from datetime import datetime

import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .PDF import PDFTableGenerator

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



class FilterableListView(ListView):
    template_name = None
    model = None
    columns = None
    filter_fields = []  # To be defined in the child views
    context_object_name = 'models'

    def parse_date(self, date_str):
        """
        Parse a date string into a datetime object.
        If the format is invalid or the value is nonsensical, return datetime.min.
        """
        try:
            # Replace backslashes with forward slashes and parse
            normalized_date = date_str.replace("\\", "/")
            return datetime.strptime(normalized_date, "%d/%m/%Y")
        except (ValueError, AttributeError):
            # Return a default date for invalid or missing values
            return datetime.min

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        # Get the ordering parameter from the GET request, default to descending
        ordering = self.request.GET.get('order', 'desc')

        # Apply filters dynamically
        for field in self.filter_fields:
            filter_value = self.request.GET.get(field)
            if filter_value:
                filters &= Q(**{f"{field}__icontains": filter_value})

        # Apply the filters
        filtered_queryset = queryset.filter(filters)

        # Parse and sort by date in Python
        models = list(filtered_queryset)
        models.sort(
            key=lambda x: self.parse_date(x.date) if x.date else datetime.min,
            reverse=(ordering == 'desc')
        )

        return models

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

class FabricView(FilterableListView):
    template_name = "cloth/balance.html"
    model = Fabric
    filter_fields = ['fabric_code', 'fabric_name', 'color']
    columns = ["التاريخ","كود الخامة","اسم الخامة","اللون","عدد الاتواب","الوزن","اسم المصبغة"]


class CutTransferView(FilterableListView):
    template_name = "cloth/cut.html"
    model = CutTransfer
    filter_fields = ['fabric_code', 'model_number']
    columns = ["الرمز","التاريخ","كود الخامة","رقم الموديل","اسم الخامة","اللون","عدد الاتواب","الوزن"]


class ReturnTransferView(FilterableListView):
    template_name = "cloth/return.html"
    model = ReturnTransfer
    filter_fields = ['fabric_code', 'model_number']
    columns = ["الرمز","التاريخ","كود الخامة","رقم الموديل","اسم الخامة","اللون","عدد الاتواب","الوزن"]


class StatisticsView(FilterableListView):
    template_name = "cloth/statistics.html"
    model = Statistics
    filter_fields = ['fabric_code', 'model_number', 'fabric_name', 'color']
    columns = ["التاريخ","كود الخامة","اسم الخامة","اللون","عدد الاتواب","الوزن","اسم المصبغة","رقم الموديل","نوع الحركة","رمز الحركة"]

