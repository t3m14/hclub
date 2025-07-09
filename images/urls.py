from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Попробуем несколько вариантов
router = DefaultRouter()
router.register(r'', views.ImageUploadViewSet, basename='image')

# Альтернативные прямые пути
urlpatterns = [
    # Стандартный роутер
    path('', include(router.urls)),
    
    # Прямые пути для отладки
    path('list/', views.ImageUploadViewSet.as_view({'get': 'list'}), name='image-list-direct'),
    path('create/', views.ImageUploadViewSet.as_view({'post': 'create'}), name='image-create-direct'),
    path('debug/', views.ImageUploadViewSet.as_view({'get': 'debug_routes'}), name='image-debug-direct'),
    
    # Пути с ID
    path('<int:pk>/', views.ImageUploadViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='image-detail-direct'),
]