
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    
    def get_queryset(self):
        queryset = Service.objects.all()
        service_type_id = self.request.query_params.get('service_type_id', None)
        
        if service_type_id:
            queryset = queryset.filter(service_type_id=service_type_id)
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        full_count = queryset.count()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            count = len(page)
            return Response({
                'result': serializer.data,
                'count': count,
                'full_count': full_count
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'result': serializer.data,
            'count': full_count,
            'full_count': full_count
        })
