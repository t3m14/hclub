# contacts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([AllowAny])  # Разрешаем всем GET-запросы
def contact_view(request):
    """
    Управление контактной информацией
    GET - получить контакты (без авторизации)
    POST - создать контакты (если не существуют) (с авторизацией)
    PUT/PATCH - обновить контакты (с авторизацией)
    """
    
    # Проверяем авторизацию только для не-GET запросов
    if request.method != 'GET' and not request.user.is_authenticated:
        return Response(
            {'error': 'Требуется авторизация для данного действия'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if request.method == 'GET':
        # Получаем первый (и единственный) объект контактов
        contact = Contact.objects.first()
        
        if not contact:
            # Если контактов нет, возвращаем пустой объект с дефолтными значениями
            return Response({
                'email': '',
                'phones': [],
                'instagram': '',
                'telegram': '',
                'whatsapp': '',
                'schedule': []
            })
        
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Проверяем, есть ли уже контакты
        if Contact.objects.exists():
            return Response(
                {'error': 'Контакты уже существуют. Используйте PUT для обновления.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method in ['PUT', 'PATCH']:
        # Получаем или создаем объект контактов
        contact = Contact.objects.first()
        
        if not contact:
            # Если контактов нет, создаем новые
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                contact = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Обновляем существующие контакты
            partial = request.method == 'PATCH'
            serializer = ContactSerializer(contact, data=request.data, partial=partial)
            if serializer.is_valid():
                contact = serializer.save()
                return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)