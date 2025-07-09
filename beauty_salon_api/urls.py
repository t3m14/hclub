from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/service_types/', include('services.urls')),  # Изменено для соответствия ТЗ
    path('api/services/', include('services.urls')),
    path('api/masters/', include('masters.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/products/', include('products.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/images/', include('images.urls')),
    path('api/random-quote/', include('quotes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)