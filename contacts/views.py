from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email']
    ordering_fields = ['email', 'created_at']
    ordering = ['-created_at']