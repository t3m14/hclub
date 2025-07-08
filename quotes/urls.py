from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
]