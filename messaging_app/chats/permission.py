from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation/message to view it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == user or obj.receiver == user
        return False
