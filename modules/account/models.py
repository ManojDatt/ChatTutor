# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db import models
from django.utils.encoding import smart_str
from rest_framework.authtoken.models import Token

class Account(AbstractUser):
	MALE = "Male"
	FEMALE = "Female"
	GENDER = (
		(MALE,'Male'),
		(FEMALE,'Female'))

	class Meta:
		verbose_name = "Account"
		verbose_name_plural = "Accounts"
	username = models.CharField(verbose_name='Username',max_length=100, unique= True)
	gender = models.CharField(verbose_name='Gender',max_length=20,choices=GENDER, blank=True, null=True)

	def __str__(self):
		return smart_str(self.username)

def assign_auth_token(sender, instance, created, **kwargs):
	if created:
		Token.objects.create(user=instance)
post_save.connect(assign_auth_token, Account)