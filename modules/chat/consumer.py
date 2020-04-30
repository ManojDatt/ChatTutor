# -*- coding: utf-8 -*-
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from .models import ChatRoom, ChatMessage as Message
from .exceptions import ClientError

from django.contrib.auth.models import AnonymousUser
from .utils import get_room_or_error, create_message, get_message_json, get_user
import pdb
from asgiref.sync import async_to_sync
from urllib import parse

class ChatConsumer(AsyncJsonWebsocketConsumer):
    # WebSocket event handlers
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        query_string = dict(self.scope).get('query_string')
        keys = dict(parse.parse_qs(query_string.decode()))
        try:
            access_token = keys.get('key')
            self.scope['user'] = await get_user(access_token[0])
            self.chat_room = self.scope['url_route']['kwargs']['channel']
            await self.accept()

        except Exception as ex:
            print(ex)
            self.scope['user'] = AnonymousUser()
            await self.close()
            

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        # try:
        command = content.get("command", None)
        if command == "join":
            await self.join_room(content)

        elif command == "send":
            await self.send_room(content)

        # except ClientError as e:
        #     # Catch any errors and send it back
        #     await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        await self.close()

   

    async def join_room(self, content):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(content.get('room'), self.scope["user"])
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the room
        await self.send_json({
            "command": "join",
            "room_number": room.room_number,
            "sender_id": self.scope["user"].id,
            "sender": self.scope["user"].username.title(),
            "receiver": content.get('receiver')
        })

    async def send_room(self, content):
        """
        Called by receive_json when someone sends a message to a room.
        """
        
        room = await get_room_or_error(content['room'], self.scope["user"])

        mesg_obj = await create_message(room, self.scope["user"], content)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "message_id": mesg_obj.id
            }
        )

    

    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        await self.send_json(
            {
                "room": event["room_id"],
                "username": event["username"],
                "sender":  event["sender"],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        serializer = await get_message_json(event['message_id'])
        print(serializer)
        await self.send_json(
            serializer,
        )