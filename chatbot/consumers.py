# chatbot/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on initial WebSocket connection.
        # We’ll use a “room name” from the URL to create a group
        self.room_name   = self.scope['url_route']['kwargs']['room_name']
        self.group_name  = f"chat_{self.room_name}"

        # Join room group (so messages sent to the group go to this socket)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the connection (otherwise it will be rejected)
        await self.accept()

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

        # Broadcast this message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',   # event name → calls chat_message()
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Called when someone has sent a message to the group
        message = event['message']

        # Send the message down the WebSocket to the client
        await self.send(text_data=json.dumps({
            'message': message
        }))
