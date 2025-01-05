from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from .api import PopulateModelsView

urlpatterns = [
    path('api/populate-models/', PopulateModelsView.as_view(), name='populate-models'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('', FabricView.as_view(), name='fabric_view'),
    path('CutTransfer/', CutTransferView.as_view(), name='cut_transfer_view'),
    path('ReturnTransfer/', ReturnTransferView.as_view(), name='return_transfer_view'),
    path('Statistics/', StatisticsView.as_view(), name='statistics_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
