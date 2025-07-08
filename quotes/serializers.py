from rest_framework import serializers
from .models import Quote, DailyQuote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'author', 'text', 'is_used', 'created_at']
        read_only_fields = ['is_used', 'created_at']


class DailyQuoteSerializer(serializers.ModelSerializer):
    quote_text = serializers.CharField(source='quote.text', read_only=True)
    quote_author = serializers.CharField(source='quote.author', read_only=True)
    
    class Meta:
        model = DailyQuote
        fields = ['id', 'quote_text', 'quote_author', 'date', 'created_at']
        read_only_fields = ['created_at']


class RandomQuoteSerializer(serializers.Serializer):
    """Сериализатор для endpoint случайной цитаты"""
    author = serializers.CharField()
    text = serializers.CharField()