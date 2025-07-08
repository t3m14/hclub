from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
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
        try:
            token = RefreshToken(value)
            return value
        except Exception:
            raise serializers.ValidationError('Неверный refresh token')
