from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .models import Message

@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # or login page
def get_threaded_replies(message):
    replies = []
    direct_replies = message.replies.select_related('sender').all()
    for reply in direct_replies:
        replies.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return replies

def conversation_view(request, message_id):
    root_message = get_object_or_404(Message, id=message_id, parent_message__isnull=True)
    thread = {
        'message': root_message,
        'replies': get_threaded_replies(root_message)
    }
    return render(request, 'messaging/conversation.html', {'thread': thread})

