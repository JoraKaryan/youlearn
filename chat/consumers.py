import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Ensure the channel layer is properly assigned
        self.channel_layer = get_channel_layer()

        if self.channel_layer is None:
            print("Channel layer is not configured.")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Check if channel_layer exists
        if self.channel_layer:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        else:
            print("Channel layer is None during disconnect.")


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    # Receive message from the room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))