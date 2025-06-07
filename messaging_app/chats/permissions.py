from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation or message to access it.

    - For messages:
        - Both sender and receiver can view (GET).
        - Only the sender can update (PUT/PATCH) or delete (DELETE).
    - For conversations:
        - All participants can view, update, or delete.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Ensure the user is authenticated
        if not user or not user.is_authenticated:
            return False

        # Handle permissions for Message objects
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            is_participant = obj.sender == user or obj.receiver == user

            if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
                return is_participant

            # Only sender can modify/delete
            return obj.sender == user

        # Handle permissions for Conversation-like objects
        if hasattr(obj, 'participants'):
            is_participant = user in obj.participants.all()

            # All participants can view/update/delete
            return is_participant

        return False
