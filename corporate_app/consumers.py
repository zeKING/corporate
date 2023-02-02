import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.db.models import Q

from .models import *
import time

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        my_id = self.scope['url_route']['kwargs']['from_id']
        other_user_id = self.scope['url_route']['kwargs']['to_id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name

        )
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'chat',
            # 'user': self.scope['user'],
            'message': 'You are now connected!'
        }))
    #
    def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    def receive(self, text_data=None, bytes_data=None):
        my_id = self.scope['url_route']['kwargs']['from_id']
        other_user_id = self.scope['url_route']['kwargs']['to_id']
        # self.accept()
        data_json = Message.objects.filter(Q(from_user_id=my_id, to_user_id=other_user_id) |
            Q(from_user_id=other_user_id, to_user_id=my_id)).first()
        # text_data_json = {
        #     'text': 'haha',
        #
        #
        # }

        # text_data_json = json.loads(text_data)
        # message = text_data['message']
        text = data_json.text
        file = data_json.file
        created = data_json.created.strftime("%d-%m-%Y %H:%M:%S")


        # print(self.scope['user'].id)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
            'type': 'chat_message',
            'text': text,
            'file': file.path,
            'created': created,

            }
        )
    def chat_message(self, event):
        text = event['text']
        file = event['file']
        created = event['created']
        self.send(text_data=json.dumps(
        {
            'type': 'chat_message',
            'message': text,
            'file': file,
            'created': created,
        }
        ))
