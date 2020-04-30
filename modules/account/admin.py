from django.contrib import admin
from .models import Account
from django import forms
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

admin.site.site_header = 'Chat Admin'
admin.site.unregister(Token)
admin.site.unregister(Group)
class AdminForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['username','email','gender','is_active','password',]

class AccountAdmin(admin.ModelAdmin):
	list_display = ('username','gender','is_active', 'date_joined',)
	readonly_fields = ('date_joined','last_login',)
	search_fields = ('username',)
	form = AdminForm
	list_filter = ('gender', 'is_active', )
	def save_model(self, request, obj, form, change):
		if obj.pk:
			orig_obj = Account.objects.get(pk=obj.pk)
			if obj.password != orig_obj.password:
				obj.set_password(obj.password)
		else:
			obj.set_password(obj.password)
		obj.save()


admin.site.register(Account, AccountAdmin)
