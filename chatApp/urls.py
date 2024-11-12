from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'', ChatViewSet, basename='chat')
router.register(r'(?P<chat_id>\d+)/messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
