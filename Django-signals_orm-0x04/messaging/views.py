from mailbox import Message
from django.shortcuts import render

# Create your views here.
# Inside a view or serializer where request.user is available
message = Message.objects.get(id=message_id)
if message.content != new_content:
    message.content = new_content
    message.edited = True
    message.edited_by = request.user  # <- This is how you track the editor
    message.save()
