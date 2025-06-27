# chatbot/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from .ai import handle_intent
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on initial WebSocket connection.
        # We’ll use a “room name” from the URL to create a group
        user = self.scope['user']
        if not user.is_authenticated:
            # Reject connection if user is not authenticated
            await self.close(code=4001)
            return
        self.room_name   = self.scope['url_route']['kwargs']['room_name']
        self.group_name  = f"chat_{self.room_name}"

        # Join room group (so messages sent to the group go to this socket)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the connection (otherwise it will be rejected)
        await self.accept()

        last_messages = await self.get_last_messages(self.room_name)
        for msg in last_messages:
            # await self.send(text_data=json.dumps({
            #     'message': msg.content,
            #     'username': msg.user.username,
            #     'timestamp': msg.timestamp.isoformat(),
            # }))
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, close_code):
        # Called when the WebSocket closes
        # Leave the room group so you stop receiving messages
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Called when a text frame is received from the client
        data = json.loads(text_data)
        message = data.get('message', '')

        user = self.scope['user']
        # saved = await self.save_message(self.room_name, user, message)

        # # Broadcast to group, including metadata
        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {
        #         'type': 'chat.message',
        #         'message': saved.content,
        #         'username': saved.user.username,
        #         'timestamp': saved.timestamp.isoformat(),
        #     }
        # )
        username = self.scope['user'].username
        saved = await self.save_message(self.room_name,self.scope['user'],message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": saved.content,
                "username": username,
                "timestamp": saved.timestamp.isoformat(),
            }
        )
    async def chat_message(self, event):
        # Send full payload to WebSocket
        await self.send(text_data=json.dumps({
            'message':   event['message'],
            'username':  event.get('username'),
            'timestamp': event.get('timestamp'),
        }))

    @database_sync_to_async
    def get_last_messages(self, room_name):
    # Fetch messages + user in one sync call, then serialize to simple dicts:
        qs = (ChatMessage.objects
            .filter(room=room_name)
            .select_related('user')
            .order_by('-timestamp')[:50])
        return [
            {
                "message":   msg.content,
                "username":  msg.user.username,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in reversed(qs)
        ]
    
    @database_sync_to_async
    def save_message(self, room, user, content):
        return ChatMessage.objects.create(room=room, user_id=user.id, content=content)

