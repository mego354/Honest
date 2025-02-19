from django.urls import path
from .views import *
from .api import PopulateModelsView


urlpatterns = [
    # path('', FabricView.as_view(), name='fabric_view'),
    # path('test/', TestView.as_view(), name='test_view'),
    # path('CutTransfer/', CutTransferView.as_view(), name='cut_transfer_view'),
    # path('ReturnTransfer/', ReturnTransferView.as_view(), name='return_transfer_view'),
    # path('Statistics/', StatisticsView.as_view(), name='statistics_view'),

    path('api/populate-models/', PopulateModelsView.as_view(), name='populate-models'),
    # path('generate_pdf/', generate_pdf, name='generate_pdf'),
]
