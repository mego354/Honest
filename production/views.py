import os
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView, CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from django.forms import modelformset_factory

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import datetime, now, localtime
from django.db import transaction
from django.db.models import Q, Sum, F
from django.contrib import messages

from .models import Model, Piece, SizeAmount, ProductionPiece, Carton, Packing
from .forms import ModelForm, ProductionForm, SizeAmountForm, ProductionPieceForm, CartonForm, PackingForm, PackingPieceForm

from django.utils.timezone import localtime, now

###############################################################################################################################
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
        cartons = []
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
            per_carton_key = f"Packing_per_carton_{index}"

            size = self.request.POST.get(size_key)
            amount = self.request.POST.get(amount_key)
            per_carton = self.request.POST.get(per_carton_key)

            if not size or not amount:  # Stop if no more sizes are found
                break

            sizes_amounts.append({"size": size, "amount": int(amount), "Packing_per_carton": int(per_carton)})
            index += 1

        # Reset index for cartons
        index = 1
        while True:
            length_key = f"carton_length_{index}"
            width_key = f"carton_width_{index}"
            height_key = f"carton_height_{index}"
            type_key = f"carton_type_{index}"
            comment_key = f"carton_comment_{index}"

            length = self.request.POST.get(length_key)
            width = self.request.POST.get(width_key)
            height = self.request.POST.get(height_key)
            carton_type = self.request.POST.get(type_key)
            comment = self.request.POST.get(comment_key)

            if not length or not width or not height or not carton_type:
                break

            cartons.append({
                "length": length,
                "width": width,
                "height": height,
                "type": carton_type,
                "comment": comment or ""
            })
            index += 1

        # Save sizes to the database
        size_amounts_objects = [
            SizeAmount(model=model, size=size_data["size"], amount=size_data["amount"], Packing_per_carton=size_data["Packing_per_carton"])
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

        # Save cartons to the database
        carton_objects = [
            Carton(model=model, **carton_data) for carton_data in cartons
        ]
        Carton.objects.bulk_create(carton_objects)

        # Add a success message
        messages.success(self.request, f"تم انشاء الموديل {model.model_number} بنجاح")
        model.update_available_carton()

        return redirect(reverse_lazy('model_detail_view', args=[model.pk]))

    def form_invalid(self, form):
        messages.error(self.request, "هنالك عطل في النموذج، يرجى إصلاحه والمحاولة مرة أخرى")
        return self.render_to_response(self.get_context_data(form=form))

class ModelDetailView(DetailView):
    model = Model
    template_name = "production/detail_model.html" 
    context_object_name = "model"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.get_object()

        context['total_Dozens'] = int(model.get_total_sizes_pieces() / 12)
        return context
    
class ModelDeleteView(DeleteView):
    model = Model
    template_name = "production/delete_model.html"
    success_url = reverse_lazy('model_list_view')

    def form_valid(self, form):
        messages.success(self.request, "تم حذف الموديل بنجاح")
        return super().form_valid(form)

class ModelUpdateView(UpdateView):
    model = Model
    form_class = ModelForm
    template_name = "production/edit_model.html"

    def form_valid(self, form):
        messages.success(self.request, "تم تعديل الموديل بنجاح")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('model_detail_view', kwargs={'pk': self.object.pk})

class BaseModelListingView(ListView):
    template_name = "production/list_model.html"
    model = Model
    paginate_by = 20
    filter_fields = ["model_number", "start_date", "end_date"]
    is_archive = False  # Default to non-archived models

    def parse_date(self, date_str):
        """Parse a date string into a datetime object."""
        try:
            normalized_date = date_str.replace("\\", "/")
            return datetime.strptime(normalized_date, "%Y-%m-%d")
        except (ValueError, AttributeError):
            return None

    def get_queryset(self):
        # for model in Model.objects.all():
        #     model.update_available_carton()
        queryset = super().get_queryset()
        filters = Q(is_archive=self.is_archive)  # Use dynamic is_archive flag

        model_number = self.request.GET.get("model_number")
        if model_number:
            filters &= Q(model_number__icontains=model_number)

        start_date = self.parse_date(self.request.GET.get("start_date"))
        end_date = self.parse_date(self.request.GET.get("end_date"))
        if start_date:
            filters &= Q(created_at__gte=start_date)
        if end_date:
            filters &= Q(created_at__lte=end_date)

        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_archive"] = self.is_archive  # Pass archive status to template
        context["filter_fields"] = [
            {"field_name": "model_number", "verbose_name": "رقم الموديل", "value": self.request.GET.get("model_number", "")},
            {"field_name": "start_date", "verbose_name": "تاريخ البداية", "value": self.request.GET.get("start_date", "")},
            {"field_name": "end_date", "verbose_name": "تاريخ النهاية", "value": self.request.GET.get("end_date", "")},
        ]
        return context

class ModelListingView(BaseModelListingView):
    is_archive = False

class ArchivedModelListingView(BaseModelListingView):
    is_archive = True
    
    
class ToggleArchiveView(View):
    def get(self, request, pk, *args, **kwargs):
        model_instance = get_object_or_404(Model, pk=pk)
        archive_mode = not model_instance.is_archive
        model_instance.is_archive = archive_mode
        model_instance.save()
        if archive_mode:
            messages.success(self.request, f"تم اضافة المودبل {model_instance.model_number} للارشيف بنجاح")
            return redirect(reverse_lazy("archived_model_list_view"))

        else:
            messages.success(self.request, f"تم ازالة المودبل {model_instance.model_number} من الارشيف بنجاح")
            return redirect(reverse_lazy("model_list_view"))

class ToggleShippedView(View):
    def get(self, request, pk, *args, **kwargs):
        model_instance = get_object_or_404(Model, pk=pk)
        shipped_mode = not model_instance.is_shipped
        model_instance.is_shipped = shipped_mode
        model_instance.shipped_at = localtime(now()) if shipped_mode else None
        model_instance.save()
        
        archive_mode = model_instance.is_archive
        if archive_mode:
            messages.success(self.request, f"تم الغاء شحن الموديل بنجاح")
            return redirect(reverse_lazy("archived_model_list_view"))
        else:
            messages.success(self.request, f"تم شحن الموديل بنجاح")
            return redirect(reverse_lazy("model_list_view"))


###############################################################################################################################
class SizeAmountCreateView(CreateView):
    model = SizeAmount
    form_class = SizeAmountForm
    template_name = "production/size_edit.html"

    def form_valid(self, form):
        model_id = self.kwargs.get("model_id")
        model = get_object_or_404(Model, pk=model_id)
        form.instance.model = model

        size_amount = form.save()

        for piece in model.pieces.all():
            if not Piece.objects.filter(model=model, type=piece.type, size=size_amount.size).exists():
                Piece.objects.create(
                    model=model,
                    type=piece.type,
                    size=size_amount.size,
                    available_amount=size_amount.amount
                )

        model.update_available_carton()
        messages.success(self.request, "تم اضافة المقاس وكل القطع المرتبطة به بنجاح.")
        return redirect(reverse_lazy("model_detail_view", args=[model_id]))
    
class SizeAmountEditView(UpdateView):
    model = SizeAmount
    form_class = SizeAmountForm
    template_name = "production/size_edit.html"

    
    def form_valid(self, form):
        size_amount = self.get_object()
        model = size_amount.model

        old_size = size_amount.size
        new_size = form.cleaned_data['size']
        new_amount = form.cleaned_data['amount'] - size_amount.amount

        form.save()

        Piece.objects.filter(model=model, size=old_size).update(
            size=new_size,
            available_amount=F('available_amount') + new_amount,
        )

        model.update_available_carton()
        messages.success(self.request, "تم تعديل المقاس وكل القطع المرتبطة به بنجاح.")
        return redirect(reverse_lazy("model_detail_view", args=[model.id]))
    
class SizeAmountDeleteView(DeleteView):
    model = SizeAmount
    template_name = "production/delete_size.html" 

    def form_valid(self, form):
        size_amount = self.get_object()
        model_pk = size_amount.model.id
        model = get_object_or_404(Model, pk=model_pk)

        pieces = Piece.objects.filter(model=size_amount.model,size=size_amount.size)
        pieces.delete()
        size_amount.delete()

        messages.success(self.request, "تم حذف المقاس وكل القطع المرتبطة به بنجاح")

        if model.size_amounts.all().count() > 0:
            model.update_available_carton()
            return redirect(reverse_lazy("model_detail_view", args=[model_pk]))
        else:
            messages.error(self.request, f"تم حذف موديل {model.model_number} لعدم توافر مقاسات اخري")
            model.delete()
            return redirect(reverse_lazy("model_list_view"))
            
    
###############################################################################################################################
class ProductionFormView(FormView):
    template_name = "production/production_form.html"
    form_class = ProductionForm

    def form_valid(self, form):
        model = form.cleaned_data['model']
        piece_type = form.cleaned_data['piece']
        factory = form.cleaned_data['factory']

        # Get all pieces of the selected type for the model
        pieces = Piece.objects.filter(model=model, type=piece_type)

        # Handling the dynamically added size quantities and comments
        for key, value in self.request.POST.items():
            if key.startswith("size_quantity_"):  # Checking for size input fields
                size_id = key.replace("size_quantity_", "")
                size = SizeAmount.objects.get(pk=size_id)

                # Find the piece for the current size and piece type
                piece = pieces.filter(size=size.size).first()
                comment_key = f"comment_{size_id}"
                comment = self.request.POST.get(comment_key, "")

                try:
                    quantity = int(value)

                    if quantity > 0 and piece:  # Only save if quantity is greater than zero and piece exists
                        ProductionPiece.objects.create(
                            piece=piece,
                            used_amount=quantity,
                            factory=factory,
                            comment=comment
                        )
                except (SizeAmount.DoesNotExist, ValueError):
                    messages.error(self.request, f"Invalid size selection or quantity for size ID {size_id}")

        # Update the model timestamp
        model.ended_at = now()
        model.save()

        messages.success(self.request, "تمت إضافة الانتاج بنجاح.")
        return redirect(reverse_lazy("production_form"))    
    
    def form_invalid(self, form):
        messages.error(self.request, "هنالك عطل في النموذج, يرجي اصلاحه و المحاولة مرة اخري")
        return self.render_to_response(self.get_context_data(form=form))


def load_sizes(request):
    model_id = request.GET.get('model_id')
    sizes = SizeAmount.objects.filter(model_id=model_id).values('id', 'size', 'amount', 'Packing_per_carton')
    return JsonResponse({'sizes': list(sizes)})

def load_model_Pieces_types(request):
    model_id = request.GET.get('model_id')
    model = Model.objects.get(id=model_id)
    types = set(model.pieces.values_list("type", flat=True))
    return JsonResponse({'types': list(types)})
# def load_model_Pieces_types(request):
#     model_id = request.GET.get('model_id')
#     model = Model.objects.get(id=model_id)
#     types = set(model.pieces.values_list("type", flat=True))
#     types_avail_amounts = []
#     for type in types:
#         piece_model = Piece.objects.filter(model=model, type=type).first()
#         types_avail_amounts.append({"type": type, "available_amount": piece_model.available_amount})
#     return JsonResponse({'types': list(types)})

def load_pieces(request):
    size_amount_id = request.GET.get('size_amount_id')
    size = SizeAmount.objects.get(pk=size_amount_id)
    pieces = Piece.objects.filter(size=size.size, model=size.model).values('id', 'type', 'available_amount')
    return JsonResponse({'pieces': list(pieces)})

def load_carton(request):
    model_id = request.GET.get('model_id')
    cartons = Carton.objects.filter(model_id=model_id).values('id', 'length', 'width', 'height', 'type')
    return JsonResponse({'cartons': list(cartons)})


class ProductionPieceCreateView(CreateView):
    model = ProductionPiece
    form_class = ProductionPieceForm
    template_name = 'production/production_piece_form.html'

    def form_valid(self, form):
        piece_id = self.kwargs.get('piece_id')
        self.piece = get_object_or_404(Piece, pk=piece_id)
        form.instance.piece = self.piece
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        model = self.piece.model
        model.ended_at = localtime(now())
        model.save()
        messages.success(self.request, "تمت إضافة الانتاج بنجاح.")
        return redirect(reverse_lazy("model_detail_view", args=[model.id]))


class ProductionPieceUpdateView(UpdateView):
    model = ProductionPiece
    form_class = ProductionPieceForm
    template_name = 'production/production_piece_form.html'

    def form_valid(self, form):
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        production_piece = self.get_object()
        model = production_piece.piece.model
        messages.success(self.request, "تم تعديل الانتاج بنجاح.")
        return redirect(reverse_lazy("model_detail_view", args=[model.id]))

class ProductionPieceDeleteView(DeleteView):
    model = ProductionPiece
    template_name = 'production/delete_production.html'

    def get_success_url(self):
        messages.success(self.request, "تم حذف الانتاج بنجاح.")
        return reverse_lazy("production_list_view")

class ProductionListingView(ListView):
    template_name = "production/list_production.html"
    model = ProductionPiece
    paginate_by = 30
    filter_fields = ["model_number", "type", "size", "start_date", "end_date", "factory"]

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

        model_number = self.request.GET.get("model_number")
        if model_number:
            filters &= Q(piece__model__model_number__icontains=model_number)

        size = self.request.GET.get("size")
        if size:
            filters &= Q(piece__size__icontains=size)

        type = self.request.GET.get("type")
        if type:
            filters &= Q(piece__type__icontains=type)

        factory = self.request.GET.get("factory")
        if factory:
            filters &= Q(factory__icontains=factory)

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
            {"field_name": "size", "verbose_name": "المقاس", "value": self.request.GET.get("size", "")},
            {"field_name": "start_date", "verbose_name": "تاريخ البداية", "value": self.request.GET.get("start_date", "")},
            {"field_name": "end_date", "verbose_name": "تاريخ النهاية", "value": self.request.GET.get("end_date", "")},
            {"field_name": "factory", "verbose_name": "المصنع", "value": self.request.GET.get("factory", "")},
        ]

        return context

###############################################################################################################################
class CartonCreateFormSetView(FormView):
    template_name = "production/carton_form_set.html"
    form_class = CartonForm

    def get_formset(self):
        """Create a formset based on the number of forms needed."""
        num_forms = int(self.request.GET.get("count", 1))
        CartonFormSet = modelformset_factory(Carton, form=CartonForm, extra=num_forms, can_delete=False)
        return CartonFormSet(queryset=Carton.objects.none())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = self.get_formset()

        return context

    def post(self, request, *args, **kwargs):
        CartonFormSet = modelformset_factory(Carton, form=CartonForm, extra=0, can_delete=False)
        formset = CartonFormSet(data=request.POST)

        model_id = self.kwargs.get("model_id")
        model = get_object_or_404(Model, pk=model_id)

        if formset.is_valid():
            for form in formset:
                carton = form.save(commit=False)
                carton.model = model
                carton.save()
            
            messages.success(self.request, "تمت إضافة الكرتون بنجاح.")
            return self.form_valid(formset)

        return self.form_invalid(formset)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("model_detail_view", args=[self.kwargs.get("model_id")])


class CartonCreateView(CreateView):
    model = Carton
    form_class = CartonForm
    template_name = 'production/carton_form.html'

    def form_valid(self, form):
        model_id = self.kwargs.get("model_id")
        self.model = get_object_or_404(Model, pk=model_id)
        form.instance.model = self.model
        form.save()

        messages.success(self.request, "تمت إضافة الكرتون بنجاح.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("model_detail_view", args=[self.model.id])


class CartonEditView(UpdateView):
    model = Carton
    form_class = CartonForm
    template_name = 'production/carton_form.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "تم تعديل الكرتون بنجاح.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        instance_carton = self.get_object()
        model = instance_carton.model
        return reverse_lazy("model_detail_view", args=[model.id])

class CartonDeleteView(DeleteView):
    model = Carton
    template_name = 'production/delete_carton.html'

    def get_success_url(self):
        instance_carton = self.get_object()
        deleted_packings = Packing.objects.filter(carton=instance_carton) 
        for deleted_packing in deleted_packings:
            deleted_packing.delete()
            
        model = instance_carton.model
        messages.success(self.request, "تم حذف الكرتون بنجاح.")
        return reverse_lazy("model_detail_view", args=[model.id])

###############################################################################################################################
class PackingFormView(FormView):
    template_name = "production/packing_form.html"
    form_class = PackingForm
            
    def form_valid(self, form):
        model_instance = form.cleaned_data['model']

        # Handling the dynamically added carton and quantities
        for key, value in self.request.POST.items():
            if key.startswith("carton_quantity_"):  # Checking for carton input fields
                carton_id = key.replace("carton_quantity_", "")
                carton_instance = Carton.objects.get(pk=carton_id)

                # Find the piece for the current size and piece type
                amount_key = f"carton_quantity_{carton_id}"
                amount = self.request.POST.get(amount_key, "")
                used_carton = int(amount)

                Packing.objects.create(
                    model=model_instance,
                    carton=carton_instance,
                    used_carton=used_carton,
                )


        messages.success(self.request, "تمت إضافة التعبئة بنجاح.")
        return redirect(reverse_lazy("production_form"))    
    
    def form_invalid(self, form):
        messages.error(self.request, "هنالك عطل في النموذج, يرجي اصلاحه و المحاولة مرة اخري")
        return self.render_to_response(self.get_context_data(form=form))


class PackingPieceUpdateView(UpdateView):
    model = Packing
    form_class = PackingPieceForm
    template_name = 'production/packing_piece_form.html'

    def form_valid(self, form):
        form.save()
        return self.get_success_url()

    def get_success_url(self):
        packing_piece = self.get_object()
        model = packing_piece.model
        model.update_available_carton()

        messages.success(self.request, "تم تعديل التعبئة بنجاح.")
        return redirect(reverse_lazy("packingpiece_edit", args=[packing_piece.id]))

class PackingPieceDeleteView(DeleteView):
    model = Packing
    template_name = 'production/delete_package.html'

    def get_success_url(self):
        packing_piece = self.get_object()
        model = packing_piece.model
        model.update_available_carton()

        messages.success(self.request, "تم حذف الانتاج بنجاح.")
        return reverse_lazy("packing_list_view")

class PackingListingView(ListView):
    template_name = "production/list_package.html"
    model = Packing
    paginate_by = 30
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

        model_number = self.request.GET.get("model_number")
        if model_number:
            filters &= Q(model__model_number__icontains=model_number)

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

###############################################################################################################################
class TestView(TemplateView):
    template_name = "production/test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        report_path = "reports/production_report.pdf"
        full_path = os.path.join(settings.MEDIA_ROOT, report_path)

        context["report_available"] = not os.path.exists(full_path)
        context["report_url"] = settings.MEDIA_URL + report_path

        return context