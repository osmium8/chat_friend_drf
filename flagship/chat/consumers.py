import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatRoom, ChatMessage
from user.models import User
from django.core.cache import cache


class ChatConsumer(AsyncWebsocketConsumer):
    def getUser(self, userId):
        return User.objects.get(id=userId)

    def getOnlineUsers(self):
        return cache.get('online_users')

    def addOnlineUser(self, user):
        try:
            if (cache.get('online_users')):
                online_user_ids: list[int] = cache.get('online_users')
                online_user_ids.append(user.id)
            else:
                online_user_ids: list[int] = [user.id]
            cache.set('online_users', online_user_ids)
        except:
            pass

    def deleteOnlineUser(self, user):
        try:
            online_user_ids: list[int] = cache.get('online_users')
            online_user_ids.remove(user)
        except:
            pass

    def saveMessage(self, message, userId, room_id):
        userObj = User.objects.get(id=userId)
        chatObj = ChatRoom.objects.get(id=room_id)
        chatMessageObj = ChatMessage.objects.create(
            chat=chatObj, user=userObj, message=message
        )
        return {
            'action': 'message',
            'user': userId,
            'room_id': room_id,
            'message': message,
            'userName': userObj.first_name + " " + userObj.last_name,
            'timestamp': str(chatMessageObj.timestamp)
        }

    async def sendOnlineUserList(self):
        onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
        chatMessage = {
            'type': 'chat_message',
            'message': {
                    'action': 'onlineUser',
                'userList': onlineUserList
            }
        }
        await self.channel_layer.group_send('onlineUser', chatMessage)

    async def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        self.userRooms = await database_sync_to_async(
            list
        )(ChatRoom.objects.filter(member=self.userId))
        for room in self.userRooms:
            print(room.id)
            await self.channel_layer.group_add(
                str(room.id),
                self.channel_name
            )
        await self.channel_layer.group_add('onlineUser', self.channel_name)
        self.user = await database_sync_to_async(self.getUser)(self.userId)
        await database_sync_to_async(self.addOnlineUser)(self.user)
        await self.sendOnlineUserList()
        await self.accept()

    async def disconnect(self, close_code):
        await database_sync_to_async(self.deleteOnlineUser)(self.user)
        await self.sendOnlineUserList()
        for room in self.userRooms:
            await self.channel_layer.group_discard(
                str(room.id),
                self.channel_name
            )

    def get_room_id(self, from_user_id, to_user_id) -> int:
        from_user = User.objects.get(id=from_user_id)
        to_user = User.objects.get(id=to_user_id)

        room = ChatRoom.objects.filter(
            member=from_user).filter(member=to_user).first()

        if (room):
            return room.id

        room = ChatRoom.objects.create(
            type="DM", name=from_user.first_name + '->' + to_user.first_name)
        room.member.add(from_user)
        room.member.add(to_user)
        room.save()

        return room.id

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        chatMessage = {}

        if action == 'message':
            # receive message for a room_id

            room_id: int = text_data_json['room_id']
            message = text_data_json['message']
            userId = text_data_json['user']
            chatMessage = await database_sync_to_async(
                self.saveMessage
            )(message, userId, room_id)
        elif action == 'typing':
            # receive typing event for a room_id

            room_id: int = text_data_json['room_id']
            chatMessage = text_data_json
        elif action == 'direct-message':
            # receive message from user_1 to user_2

            from_user_id = text_data_json['from']
            to_user_id = text_data_json['to']
            room_id: int = await database_sync_to_async(self.get_room_id)(from_user_id, to_user_id)
            
            if (to_user_id not in self.getOnlineUsers()):
                chatMessage = "The user is offline"
            else:
                message = text_data_json['message']
                chatMessage = await database_sync_to_async(self.saveMessage)(message,from_user_id, room_id)

        await self.channel_layer.group_send(
            str(room_id),
            {
                'type': 'chat_message',
                'message': chatMessage
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
