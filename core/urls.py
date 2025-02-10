from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from cloth.views import FabricView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', FabricView.as_view(), name='fabric_view'),
    path('cloth/', include('cloth.urls')),
    path('production/', include('production.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
