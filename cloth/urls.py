from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from .api import PopulateModelsView

urlpatterns = [
    path('api/populate-models/', PopulateModelsView.as_view(), name='populate-models'),
    path('', fabric_view, name='fabric_view'),
    path('CutTransfer/', cut_transfer_view, name='cut_transfer_view'),
    path('ReturnTransfer/', return_transfer_view, name='return_transfer_view'),
    path('Statistics/', statistics_view, name='statistics_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
