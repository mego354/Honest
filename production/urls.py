from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', ModelListingView.as_view(), name='model_list_view'),
    path('create/', ModelCreationView.as_view(), name='model_creation_view'),
    path('model/<int:pk>/', ModelDetailView.as_view(), name='model_detail_view'),
    path('model/<int:pk>/delete/', ModelDeleteView.as_view(), name='model_delete_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
