from django.contrib import messages  # Import the messages framework
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, DeleteView
from django.db import transaction

from .models import Model, Piece, SizeAmount
from .forms import ModelForm

class ModelCreationView(FormView):
    template_name = "production/create_model.html"
    form_class = ModelForm
    success_url = reverse_lazy("orders:success")

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
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Add an error message
        messages.error(self.request, "هنالك عطل في النموذج, يرجي اصلاحه و المحاولة مرة اخري")

        return self.render_to_response(self.get_context_data(form=form))

class ModelListingView(ListView):
    template_name = "production/list_model.html"
    model = Model
    paginate_by = 20
    
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
        messages.success(self.request, "")
        return super().form_valid(form)
