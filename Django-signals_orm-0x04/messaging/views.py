from mailbox import Message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

# Create your views here.
# Inside a view or serializer where request.user is available
message = Message.objects.get(id=message_id)
if message.content != new_content:
    message.content = new_content
    message.edited = True
    message.edited_by = request.user  # <- This is how you track the editor
    message.save()
@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # Or redirect to login page after logout
