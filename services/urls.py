from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'types', views.ServiceTypeViewSet, basename='servicetype')
router.register(r'', views.ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]