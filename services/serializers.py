from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        count = Service.objects.count()
        full_count = Service.objects.all().count()
        return {
            'result': data,
            'count': count,
            'full_count': full_count
        }
