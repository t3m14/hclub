from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Quote, DailyQuote
from .serializers import RandomQuoteSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def random_quote_view(request):
    """Получение случайной цитаты на день"""
    daily_quote = DailyQuote.get_today_quote()
    
    if daily_quote and daily_quote.quote:
        response_data = {
            'author': daily_quote.quote.author,
            'text': daily_quote.quote.text
        }
        serializer = RandomQuoteSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Цитата не найдена'}, 
        status=status.HTTP_404_NOT_FOUND
    )