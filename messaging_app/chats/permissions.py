from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow access only to participants involved in the message or conversation.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If the object has participants (e.g., a Conversation model)
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If the object is a Message with sender and receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == user or obj.receiver == user

        return False
