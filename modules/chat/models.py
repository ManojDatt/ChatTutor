# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from django.utils.encoding import smart_str
from modules.account.models import Account
from random import choice

def room_number():
    randompass = ''.join([choice('1234567890abcdefghijklmnopqrstuvwxyz') for i in range(10)])
    return randompass.upper()

class ChatRoom(models.Model):
	class Meta:
		verbose_name_plural = 'Chat Room'
	owner = models.ForeignKey(Account, null=True, blank=True,on_delete=models.CASCADE)
	guest = models.ForeignKey(Account, null=True, blank=True,on_delete=models.CASCADE, related_name="chatroom_guest")
	created_at = models.DateTimeField(auto_now=True)
	room_number = models.CharField(verbose_name='Room Number',max_length=20, default=room_number)

	def __str__(self):
		return smart_str(self.room_number)

	@property
	def group_name(self):
		return "room-%s" % self.room_number
		
class ChatMessage(models.Model):
	class Meta:
		ordering = ('-message_at',)

	sender = models.ForeignKey(Account, null=True, blank=True,on_delete=models.CASCADE)
	receiver = models.ForeignKey(Account, null=True, blank=True,on_delete=models.CASCADE, related_name="message_receiver")
	room = models.ForeignKey(ChatRoom, null=True, blank=True,on_delete=models.CASCADE)
	message = models.TextField(verbose_name='Chat Message',default="")
	message_at = models.DateTimeField(auto_now=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)
