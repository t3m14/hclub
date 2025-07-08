from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, TokenSerializer, RefreshTokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Авторизация пользователя"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Создание токенов
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        response_data = {
            'access_token': str(access_token),
            'refresh_token': str(refresh)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """Обновление access токена"""
    serializer = RefreshTokenSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            refresh_token = RefreshToken(serializer.validated_data['refresh_token'])
            
            # Создание нового access токена
            new_access_token = refresh_token.access_token
            
            # Создание нового refresh токена (ротация)
            refresh_token.blacklist()
            new_refresh_token = RefreshToken.for_user(refresh_token.payload['user_id'])
            
            response_data = {
                'access_token': str(new_access_token),
                'refresh_token': str(new_refresh_token)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': 'Неверный refresh token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)