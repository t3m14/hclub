from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, TokenSerializer, RefreshTokenSerializer

User = get_user_model()


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
            # Получаем refresh token из валидированных данных
            refresh_token_str = serializer.validated_data['refresh_token']
            
            # Создаем объект RefreshToken
            refresh_token = RefreshToken(refresh_token_str)
            
            # Получаем пользователя из токена
            user_id = refresh_token.payload.get('user_id')
            if not user_id:
                return Response(
                    {'error': 'Неверный refresh token - отсутствует user_id'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Проверяем, что пользователь существует
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Пользователь не найден'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Создание нового access токена
            new_access_token = refresh_token.access_token
            
            # Создание нового refresh токена (ротация токенов)
            new_refresh_token = RefreshToken.for_user(user)
            
            # Добавляем старый токен в черный список (если включено BLACKLIST_AFTER_ROTATION)
            try:
                refresh_token.blacklist()
            except AttributeError:
                # Если blacklist не установлен, игнорируем
                pass
            
            response_data = {
                'access_token': str(new_access_token),
                'refresh_token': str(new_refresh_token)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except TokenError as e:
            return Response(
                {'error': f'Неверный refresh token: {str(e)}'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except InvalidToken as e:
            return Response(
                {'error': f'Недействительный refresh token: {str(e)}'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка при обновлении токена: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)