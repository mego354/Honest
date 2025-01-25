from django.views.generic import FormView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.timezone import datetime
from django.db import transaction
from django.db.models import Q
from django.contrib import messages

from .models import Model, Piece, SizeAmount
from .forms import ModelForm, SizeAmountForm



class ModelCreationView(FormView):
    template_name = "production/create_model.html"
    form_class = ModelForm

    @transaction.atomic
    def form_valid(self, form):
        # Save the main model
        model = form.save()

        # Extract pieces and sizes data from POST
        pieces = []
        sizes_amounts = []
        index = 1

        # Extract piece fields
        while True:
            piece_type_key = f"piece_type_{index}"
            piece_type = self.request.POST.get(piece_type_key)

            if not piece_type:  # Stop if no more pieces are found
                break

            pieces.append({"type": piece_type})
            index += 1

        # Reset index for sizes
        index = 1
        while True:
            size_key = f"size_{index}"
            amount_key = f"amount_{index}"

            size = self.request.POST.get(size_key)
            amount = self.request.POST.get(amount_key)

            if not size or not amount:  # Stop if no more sizes are found
                break

            sizes_amounts.append({"size": size, "amount": int(amount)})
            index += 1

        # Save sizes to the database
        size_amounts_objects = [
            SizeAmount(model=model, size=size_data["size"], amount=size_data["amount"])
            for size_data in sizes_amounts
        ]
        SizeAmount.objects.bulk_create(size_amounts_objects)

        # Save pieces to the database
        for piece_data in pieces:
            for size_amount in size_amounts_objects:
                Piece.objects.create(
                    model=model,
                    type=piece_data["type"],
                    size=size_amount.size,
                    available_amount=size_amount.amount,
                )

        # Add a success message
        messages.success(self.request, f"تم انشاء المودبل {model.model_number} بنجاح")
        return redirect(reverse_lazy("model_detail_view", args=[model.pk]))
        

    def form_invalid(self, form):
        messages.error(self.request, "هنالك عطل في النموذج, يرجي اصلاحه و المحاولة مرة اخري")
        return self.render_to_response(self.get_context_data(form=form))

class ModelListingView(ListView):
    template_name = "production/list_model.html"
    model = Model
    paginate_by = 20
    filter_fields = ["model_number", "start_date", "end_date"]

    def parse_date(self, date_str):
        """
        Parse a date string into a datetime object.
        If the format is invalid or the value is nonsensical, return datetime.min.
        """
        try:
            normalized_date = date_str.replace("\\", "/")
            return datetime.strptime(normalized_date, "%Y-%m-%d")
        except (ValueError, AttributeError):
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = Q()

        # Filter by model_number (icontains)
        model_number = self.request.GET.get("model_number")
        if model_number:
            filters &= Q(model_number__icontains=model_number)

        # Filter by date range
        start_date = self.parse_date(self.request.GET.get("start_date"))
        end_date = self.parse_date(self.request.GET.get("end_date"))
        if start_date:
            filters &= Q(created_at__gte=start_date)
        if end_date:
            filters &= Q(created_at__lte=end_date)

        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filters to the context
        context["filter_fields"] = [
            {"field_name": "model_number", "verbose_name": "رقم الموديل", "value": self.request.GET.get("model_number", "")},
            {"field_name": "start_date", "verbose_name": "تاريخ البداية", "value": self.request.GET.get("start_date", "")},
            {"field_name": "end_date", "verbose_name": "تاريخ النهاية", "value": self.request.GET.get("end_date", "")},
        ]

        return context
    
class ModelDetailView(DetailView):
    model = Model
    template_name = "production/detail_model.html" 
    context_object_name = "model"
    
class ModelDeleteView(DeleteView):
    model = Model
    template_name = "production/delete_model.html"
    success_url = reverse_lazy('model_list_view')

    def form_valid(self, form):
        messages.success(self.request, "تم حذف الموديل بنجاح")
        return super().form_valid(form)
 
class SizeAmountDeleteView(DeleteView):
    model = SizeAmount
    template_name = "production/delete_size.html" 

    def form_valid(self, form):
        size_amount = self.get_object()
        model_pk = size_amount.model.id
        pieces = Piece.objects.filter(model=size_amount.model,size=size_amount.size)
        pieces.delete()
        size_amount.delete()

        messages.success(self.request, "تم حذف المقاس وكل القطع المرتبطة به بنجاح")
        return redirect(reverse_lazy("model_detail_view", args=[model_pk]))
    
class SizeAmountEditView(UpdateView):
    model = SizeAmount
    form_class = SizeAmountForm
    template_name = "production/size_edit.html"

    
    def form_valid(self, form):
        size_amount = self.get_object()
        model = size_amount.model

        old_size = size_amount.size
        new_size = form.cleaned_data['size']
        new_amount = form.cleaned_data['amount']

        form.save()
        Piece.objects.filter(model=model, size=old_size).update(size=new_size, available_amount=new_amount)

        messages.success(self.request, "تم تعديل المقاس وكل القطع المرتبطة به بنجاح.")
        return redirect(reverse_lazy("model_detail_view", args=[model.id]))