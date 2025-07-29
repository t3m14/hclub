
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'email', 'phones', 'instagram', 'telegram',
            'whatsapp', 'schedule'
        ]
    
    def validate_email(self, value):
        """Валидация email - обязательное поле"""
        if not value:
            raise serializers.ValidationError("Email обязателен")
        return value
    
    def validate_phones(self, value):
        """Валидация телефонов - первый телефон обязателен"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Phones должен быть массивом")
        
        if len(value) == 0 or not value[0]:
            raise serializers.ValidationError("Первый телефон обязателен")
        
        # Проверяем, что первый телефон не пустой
        if not value[0].strip():
            raise serializers.ValidationError("Первый телефон не может быть пустым")
        
        return value
    
    def validate_schedule(self, value):
        """Валидация расписания"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Schedule должен быть массивом")
        
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Каждый элемент расписания должен быть объектом")
            
            required_fields = ['week_day', 'hours']
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f"Поле '{field}' обязательно для расписания")
        
        return value
