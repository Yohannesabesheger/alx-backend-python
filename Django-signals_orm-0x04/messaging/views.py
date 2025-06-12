from mailbox import Message
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
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
@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_message')
        parent_message = Message.objects.get(id=parent_id) if parent_id else None

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            timestamp=timezone.now(),
            parent_message=parent_message
        )
        return redirect('inbox')  # or wherever you want to redirect

    return render(request, 'messaging/send_message.html', {'receiver': receiver})
login_required
def inbox(request):
    # Fetch messages where the logged-in user is the receiver
    # Use select_related to optimize foreign key lookups (sender and receiver)
    messages = (
        Message.objects
        .filter(receiver=request.user)
        .select_related('sender', 'receiver', 'parent_message')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})
@login_required
def user_inbox(request):
    # Get all messages received by the logged-in user
    user_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')

    return render(request, 'messaging/inbox.html', {'messages': user_messages})
@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).select_related('sender').order_by('-timestamp')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})
@login_required
def unread_messages_view(request):
    unread_messages = (
        Message.unread
        .unread_for_user(request.user)
        .select_related('sender')
        .only('id', 'sender', 'content', 'timestamp')  # explicitly in view now
        .order_by('-timestamp')
    )
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})