from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Initialize the router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Routes definition
urlpatterns = [
    path('', include(router.urls)),
]
