from rest_framework.views import APIView
from modules.account.models import Account
from modules.chat.models import ChatRoom, ChatMessage
from rest_framework.response import Response
from modules.chat.serializers import UserSerializer, ChatMessageSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
from django.db.models import Q

class GeChatRoomNumber(APIView):
	def get(self, request, user):
		owner = request.user
		guest = Account.objects.get(id=user)
		chat_rooms = ChatRoom.objects.filter(Q(owner=owner, guest=guest)|Q(owner=guest, guest=owner))
		if chat_rooms.exists():
			chat_room = chat_rooms.first()
		else:
			chat_room = ChatRoom.objects.create(owner=owner, guest=guest)
		return Response({'message': 'Chat room number fecthed successfully', 'code': 200, 'data': {'room_number': chat_room.room_number, 'room_id': chat_room.id }})

class ChatMessageList(APIView):
	def get(self, request, room_number):
		try:
			chatroom = ChatRoom.objects.get(room_number=room_number)
			chat_message_list = chatroom.chatmessage_set.all().order_by('message_at')
			paginator = LimitOffsetPagination()
			queryset_serializer_data = paginator.paginate_queryset(chat_message_list, request)
			serializers = ChatMessageSerializer(queryset_serializer_data, many=True)
			return Response({'message': 'Message list fetched successfully', 'code': 200, 'data': serializers.data, 'limit': paginator.limit,'offset': paginator.offset, 'overall_count': paginator.count})
		except Exception as ex:
			return Response({'message': str(ex), 'code': 500, 'data': []})