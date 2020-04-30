from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('account/', include('modules.account.urls')),
    path('chat/',include('modules.chat.urls')),
]