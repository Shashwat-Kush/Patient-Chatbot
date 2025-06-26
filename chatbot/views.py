from django.shortcuts import render


def index(request):
    return render(request, "chatbot/index.html", {"room_name": "lobby"})
def chat_room(request, room_name="lobby"):
    return render(request, 'chatbot/chat_room.html', { 'room_name': room_name })

