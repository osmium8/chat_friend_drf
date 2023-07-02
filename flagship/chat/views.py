from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from chat.models import ChatRoom, ChatMessage
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.core.cache import cache
from user.models import User
from user.serializers import UserSerializer


class ChatRoomView(APIView):
    def get(self, request, user_id):
        chat_rooms = ChatRoom.objects.filter(member=user_id)
        serializer = ChatRoomSerializer(
            chat_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.\
            filter(chat__id=room_id).order_by('-timestamp')


class ActivityView(APIView):

    def get(self, request):
        online_user_id: list[int] = cache.get('online_users')

        if (online_user_id is None):
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        online_user: list[User] = [
            user for user in User.objects.filter(id__in=online_user_id)]
        response = {'online_users': UserSerializer(
            online_user, many=True).data}
        return Response(response, status=status.HTTP_200_OK)