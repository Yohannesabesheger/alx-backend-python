from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Root router for conversations
router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router: messages inside conversations
convo_router = NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet,
                      basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]
