from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import formset_factory
from .models import Model, Piece, SizeAmount
from .forms import ModelForm, DynamicPieceForm, SizeAmountForm
from django.views.generic import FormView

class Model_Creation(FormView):
    template_name = "production/create.html"
    form_class = ModelForm
    success_url = "/orders/success/"     

    def form_valid(self, form):
        # Save the main order
        model = form.save()


        # return redirect(self.success_url)
        return HttpResponse('ok')

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Log form errors for debugging

        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# # Get carton data from POST request
# carton_count = int(self.request.POST.get('carton-count', 0))

# for i in range(carton_count):
#     # Dynamically retrieve data for each carton
#     size = self.request.POST.get(f'carton[{i}][size]')
#     carton_type = self.request.POST.get(f'carton[{i}][type]')
#     amount = self.request.POST.get(f'carton[{i}][amount]')
#     length = self.request.POST.get(f'carton[{i}][length]')
#     width = self.request.POST.get(f'carton[{i}][width]')
#     height = self.request.POST.get(f'carton[{i}][height]')

#     # Create and save a Carton instance
#     Carton.objects.create(
#         order=order,
#         size=size,
#         type='vegetable',
#         amount=amount,
#         length=length,
#         width=width,
#         height=height,
#     )
