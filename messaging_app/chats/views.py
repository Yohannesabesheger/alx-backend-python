from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from rest_framework.status import HTTP_403_FORBIDDEN
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    Supports filtering and search.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages filtered by conversation.
    Supports filtering by participant username and message sent date range,
    search in message_body, ordering by sent_at, and paginated results.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        if not conversation_id:
            return Message.objects.none()

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        return Message.objects.filter(conversation=conversation).order_by('-sent_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
