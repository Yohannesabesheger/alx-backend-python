from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass123')
        self.receiver = User.objects.create_user(username='receiver', password='pass123')

    def test_notification_created_on_message(self):
        """Ensure a Notification is created when a Message is sent."""
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        notif = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertEqual(notif.count(), 1)
        self.assertFalse(notif.first().is_read)
