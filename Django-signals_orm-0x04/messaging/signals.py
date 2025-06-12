from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_delete

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to create a Notification when a new Message is created."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
@receiver(post_save, sender=Message)
def log_message_edit(sender, instance, created, **kwargs):
    """Signal to log message edits."""
    if not created and instance.edited:
        MessageHistory.objects.create(
            message=instance,
            old_content=instance.content
        )
        instance.edited = True
        instance.save()
class MessageEditLoggingTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Original Message")

    def test_edit_logging_creates_history(self):
        self.message.content = "Edited Message"
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original Message")
        self.assertTrue(self.message.edited)

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications belonging to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to messages sent/received by the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()