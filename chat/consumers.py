import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
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
        if hasattr(self, 'channel_layer') and self.channel_layer:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = text_data_json['sender']
            message_id = text_data_json.get('message_id', str(time.time()))

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    'message_id': message_id
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
                'message_id': event['message_id']
            }))
        except Exception as e:
            print(f"Error in chat_message: {e}")