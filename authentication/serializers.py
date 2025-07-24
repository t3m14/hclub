from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    login = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('login')  # В ТЗ поле называется login, но это email
        password = attrs.get('password')
        
        if email and password:
            # Аутентификация по email
            user = authenticate(request=self.context.get('request'), 
                              username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Неверные учетные данные')
            
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт отключен')
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Необходимо указать email и пароль')


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    def validate_refresh_token(self, value):
        """Валидация refresh token"""
        if not value:
            raise serializers.ValidationError('Refresh token обязателен')
        
        try:
            # Проверяем, что токен валидный
            token = RefreshToken(value)
            
            # Проверяем, что токен содержит user_id
            user_id = token.payload.get('user_id')
            if not user_id:
                raise serializers.ValidationError('Неверный refresh token - отсутствует user_id')
            
            # Проверяем, что пользователь существует
            if not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError('Пользователь не найден')
            
            return value
            
        except TokenError:
            raise serializers.ValidationError('Неверный или истекший refresh token')
        except Exception as e:
            raise serializers.ValidationError(f'Ошибка валидации токена: {str(e)}')