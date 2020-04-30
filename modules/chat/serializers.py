from rest_framework import serializers
from django.conf import settings
from modules.account.models import Account
from modules.chat.models import ChatRoom, ChatMessage
from django.utils.timezone import localtime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username','gender',)

class ChatMessageSerializer(serializers.ModelSerializer):
    message_on = serializers.SerializerMethodField()
    sender_detail = serializers.SerializerMethodField()
    receiver_detail = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ('id', 'room_number','sender_detail', 'receiver_detail','message','message_on','seen',)

    def get_message_on(self, obj):
        return localtime(obj.message_at).strftime('%H:%M %p %d-%m-%Y')

    def get_sender_detail(self, obj):
        return UserSerializer(obj.sender).data

    def get_receiver_detail(self, obj):
        return UserSerializer(obj.receiver).data

    def get_room_number(self, obj):
        return obj.room.room_number