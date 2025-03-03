from django.urls import path
from .api_views import AllDataAPIView

urlpatterns = [
    path('all-data/', AllDataAPIView.as_view(), name='all-data'),
]