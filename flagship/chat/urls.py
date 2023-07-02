from django.urls import path
from chat.views import ChatRoomView, MessagesView, ActivityView

urlpatterns = [
	path('chats', ChatRoomView.as_view(), name='chatRoom'),
	path('chats/<str:room_id>/messages', MessagesView.as_view(), name='messageList'),
	path('users/<int:user_id>/chats', ChatRoomView.as_view(), name='chatRoomList'),
    path('activity/online-users',ActivityView.as_view(), name='onlineUsers'),
]