from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'parent_message', 'timestamp')
    list_filter = ('sender', 'receiver')

admin.site.register(Message, MessageAdmin)
