from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', ModelListingView.as_view(), name='model_list_view'),
    path('test/', TestView.as_view(), name='test_view'),
    path('archive-models/', ArchivedModelListingView.as_view(), name='archived_model_list_view'),
    path('create/', ModelCreationView.as_view(), name='model_creation_view'),
    path('model/<int:pk>/', ModelDetailView.as_view(), name='model_detail_view'),
    path('model/<int:pk>/edit', ModelUpdateView.as_view(), name='model_update_view'),
    path('model/<int:pk>/delete/', ModelDeleteView.as_view(), name='model_delete_view'),
    path('model/<int:pk>/toggle-archive/', ToggleArchiveView.as_view(), name='toggle_archive'),

    path('model/<int:pk>/add-carton', CartonCreateView.as_view(), name='add_carton_view'),
    
    path('size/add/<int:model_id>/', SizeAmountCreateView.as_view(), name='sizeamount_add'),
    path('size/<int:pk>/edit/', SizeAmountEditView.as_view(), name='SizeAmount_edit'),
    path('size/<int:pk>/delete/', SizeAmountDeleteView.as_view(), name='SizeAmount_delete_view'),

    path('production-list', ProductionListingView.as_view(), name='production_list_view'),
    path('production/add/<int:piece_id>/', ProductionPieceCreateView.as_view(), name='productionpiece_add'),
    path('production/<int:pk>/edit/', ProductionPieceUpdateView.as_view(), name='productionpiece_edit'),
    path('production/<int:pk>/delete/', ProductionPieceDeleteView.as_view(), name='productionpiece_delete'),

    path('production/', ProductionFormView.as_view(), name='production_form'),
    path('load-sizes/', load_sizes, name='load_sizes'),
    path('load-pieces/', load_pieces, name='load_pieces'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
