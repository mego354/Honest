from django.views.generic.list import ListView
from django.db.models import Q
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics, Updates

from django.utils.timezone import localtime
from datetime import datetime

class FilterableListView(ListView):
    template_name = None
    model = None
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

class CutTransferView(FilterableListView):
    template_name = "cloth/cut.html"
    model = CutTransfer
    filter_fields = ['fabric_code', 'model_number']

class ReturnTransferView(FilterableListView):
    template_name = "cloth/return.html"
    model = ReturnTransfer
    filter_fields = ['fabric_code', 'model_number']

class StatisticsView(FilterableListView):
    template_name = "cloth/statistics.html"
    model = Statistics
    filter_fields = ['fabric_code', 'model_number']
