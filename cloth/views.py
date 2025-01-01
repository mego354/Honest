from django.views.generic.list import ListView
from django.db.models import Q
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics, Updates

class FilterableListView(ListView):
    template_name = None
    model = None
    filter_fields = []  # To be defined in the child views
    context_object_name = 'models'

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        # Get the ordering parameter from the GET request, default to descending
        ordering = self.request.GET.get('order', 'desc')
        order_by_field = '-date' if ordering == 'desc' else 'date'

        # Loop through each filter field and apply it dynamically
        for field in self.filter_fields:
            filter_value = self.request.GET.get(field)
            if filter_value:
                filters &= Q(**{f"{field}__icontains": filter_value})

        return queryset.filter(filters).order_by(order_by_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Format the date in the desired string format
        update = Updates.objects.all().order_by('-date').first()
        context['update'] = update.date.strftime("%d/%m %I:%M %p") if update and update.date else None
        
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
    filter_fields = ['fabric_code', 'fabric_name']

class StatisticsView(FilterableListView):
    template_name = "cloth/statistics.html"
    model = Statistics
    filter_fields = ['fabric_code', 'model_number']
