from django.urls import path
from .views import GeChatRoomNumber, ChatMessageList

urlpatterns = [
	path('get-room/<int:user>', GeChatRoomNumber.as_view()),
	path('<str:room_number>/messages', ChatMessageList.as_view()),
]