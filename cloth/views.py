from django.views.generic.list import ListView
from django.db.models import Q
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics, Updates

class FilterableListView(ListView):
    template_name = None
    model = None 
    filter_field_1 = 'fabric_code'
    filter_field_2 = 'model_number'
    context_object_name = 'models'

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()
        ordering = self.request.GET.get('order', 'desc')  # Default to descending
        order_by_field = '-date' if ordering == 'desc' else 'date'

        # Apply filters for the specified fields
        filter_value_1 = self.request.GET.get(self.filter_field_1)
        filter_value_2 = self.request.GET.get(self.filter_field_2)

        if filter_value_1:
            filters &= Q(**{f"{self.filter_field_1}__icontains": filter_value_1})
        if filter_value_2:
            filters &= Q(**{f"{self.filter_field_2}__icontains": filter_value_2})

        return queryset.filter(filters).order_by(order_by_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve verbose names for the filter fields
        model_meta = self.model._meta
        context['filter_field_1'] = {
            'field_name': self.filter_field_1,
            'verbose_name': model_meta.get_field(self.filter_field_1).verbose_name,
            'value': self.request.GET.get(self.filter_field_1) or "",
        }
        context['filter_field_2'] = {
            'field_name': self.filter_field_2,
            'verbose_name': model_meta.get_field(self.filter_field_2).verbose_name,
            'value': self.request.GET.get(self.filter_field_2) or "",
        }
        return context

class FabricView(FilterableListView):
    template_name = "cloth/balance.html"
    model = Fabric
    filter_field_2 = 'fabric_name'

class CutTransferView(FilterableListView):
    template_name = "cloth/cut.html"
    model = CutTransfer

class ReturnTransferView(FilterableListView):
    template_name = "cloth/return.html"
    model = ReturnTransfer

class StatisticsView(FilterableListView):
    template_name = "cloth/statistics.html"
    model = Statistics
