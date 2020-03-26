import asyncio
import json
from .models import Thread, ChatMessage

from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connect", event)
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        # print("User typeeee: ", me.__class__)

        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chatroom = f"thread_{thread_obj.id}"
        self.chatroom = chatroom
        await self.channel_layer.group_add(chatroom, self.channel_name)
        await self.send({"type" : "websocket.accept"})

    async def websocket_disconnect(self, event):
        print("disconnected")

    async def websocket_receive(self, event):
        print("received...", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            user = self.scope['user']
            username = 'error'
            msg = loaded_dict_data.get('message')
            if user.is_authenticated:
                username = user.username
             
            if msg is None:
                
                if self.scope['user'] == await self.get_first():
                    print("yaaa")
                    self.thread_obj.seen_by_first = 'y'
                    await self.save_thread()
                if self.scope['user'] == await self.get_second():
                    print("yoooo")
                    self.thread_obj.seen_by_second = 'y'
                    await self.save_thread()
                print("Finallyyyyyy")
                return 
            
            if username == loaded_dict_data.get('sender'):
                    print("haaaannnnnn")
                    self.thread_obj.seen_by_first = 'n'
                    self.thread_obj.seen_by_second = 'n'
                    await self.save_thread()
                    
            myResponse = {
                'message' : msg,
                'username' : username
            }
        else:
            print("haan pahuchyu")
        await self.create_chat_message(msg)
        await self.channel_layer.group_send(
            self.chatroom,
            {
                "type" : "chat_message",
                "text" : json.dumps(myResponse)
            }
        )
        

    async def chat_message(self, event):
        await self.send({"type" : "websocket.send", "text": event['text']})

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, msg):
        return ChatMessage.objects.create(thread= self.thread_obj, user = self.scope['user'], message = msg)


    @database_sync_to_async
    def get_first(self):
        return self.thread_obj.first

    @database_sync_to_async
    def get_second(self):
        return self.thread_obj.second

    @database_sync_to_async
    def save_thread(self):
        self.thread_obj.save()

