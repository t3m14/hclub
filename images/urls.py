from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ImageUploadViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls), {'http_method_names': ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']}),
]