from django.urls import path
from .views import chat_room

urlpatterns = [
    path('chat/<str:room_name>/', chat_room, name='chat-room'),
]