from django.contrib import admin
from modules.account.models import Account
from .models import ChatRoom, ChatMessage
from django import forms

class ChatMessageInline(admin.TabularInline):
	model = ChatMessage
	extra = 0
	fields = ('sender','receiver','room','message','message_at','seen',)
	
	def get_readonly_fields(self, request, obj=None):
		readonly_fields = list(set(
			[field.name for field in self.opts.local_fields] +
			[field.name for field in self.opts.local_many_to_many]
		))
		
		return readonly_fields
	def has_add_permission(self, request, *args, **kwargs):
		return False


class ChatAdmin(admin.ModelAdmin):
	list_display = ['owner','guest','room_number']
	inlines = [ChatMessageInline]

	def has_add_permission(self, request, *args, **kwargs):
		return False

		

admin.site.register(ChatRoom, ChatAdmin)