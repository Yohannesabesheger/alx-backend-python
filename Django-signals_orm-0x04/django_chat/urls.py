from django.urls import path
from .views import conversation_view

urlpatterns = [
    path('conversation/<int:message_id>/', conversation_view, name='conversation_view'),
]