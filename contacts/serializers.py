from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'email', 'phones', 'instagram', 'telegram',
            'whatsapp', 'schedule'
        ]
        # Убираем id, created_at, updated_at из ответа
    
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
