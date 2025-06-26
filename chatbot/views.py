from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def chat_room(request, room_name="lobby"):
    return render(request, 'templates/chatbot/index.html', { 'room_name': room_name })
