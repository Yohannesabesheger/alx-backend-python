import django_filters
from django_filters.rest_framework import FilterSet
from .models import Message

class MessageFilter(FilterSet):
    conversation_participant = django_filters.CharFilter(
        field_name='conversation__participants__username', lookup_expr='icontains'
    )
    sent_at__gte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation_participant', 'sent_at__gte', 'sent_at__lte']
