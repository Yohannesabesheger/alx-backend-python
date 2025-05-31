from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicitly declare fields with CharField
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email',
                  'first_name', 'last_name', 'phone_number']

    # Example of custom validation on username
    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError(
                "Username must not contain spaces.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.CharField(read_only=True)
    message_body = serializers.CharField()
    sent_at = serializers.CharField(read_only=True)
    # Nested sender info as a read-only SerializerMethodField
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender',
                  'conversation', 'message_body', 'sent_at']

    def get_sender(self, obj):
        # Return a simplified sender representation
        return {
            'user_id': str(obj.sender.user_id),
            'username': obj.sender.username,
            'email': obj.sender.email
        }


class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    # Show participants as nested users
    participants = UserSerializer(many=True)
    # Show messages using MessageSerializer
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants.")
        return value
