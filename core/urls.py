from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from cloth.views import IndexView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index_view'),
    path('cloth/', include('cloth.urls')),
    path('production/', include('production.urls')),
    path('accessories/', include('accessories.urls')),
    path('api/', include('api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
