import django_filters
from django_filters.rest_framework import FilterSet, filters
from .models import Message, Conversation

class MessageFilter(FilterSet):
    # Filter messages by date range
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    # Optionally filter by conversation participant username or email
    participant = filters.CharFilter(method='filter_by_participant')

    class Meta:
        model = Message
        fields = ['conversation', 'start_date', 'end_date']

    def filter_by_participant(self, queryset, name, value):
        # Filter messages where sender or receiver username or email matches value
        return queryset.filter(
            conversation__participants__username__icontains=value
        ) | queryset.filter(
            conversation__participants__email__icontains=value
        )
