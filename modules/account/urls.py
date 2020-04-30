from django.urls import path
from .views import Login, AccountList

urlpatterns = [
	path('login', Login.as_view()),
	path('all', AccountList.as_view()),
]