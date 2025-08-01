from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('backend/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API endpoints
    path('backend/auth/', include('authentication.urls')),
    path('backend/service_types/', include('service_types.urls')),  # Изменено для соответствия ТЗ
    path('backend/services/', include('services.urls')),
    path('backend/masters/', include('masters.urls')),
    path('backend/portfolio/', include('portfolio.urls')),
    path('backend/products/', include('products.urls')),
    path('backend/contacts/', include('contacts.urls')),
    path('backend/images/', include('images.urls')),
    path('backend/random-quote/', include('quotes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)