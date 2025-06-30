from django.urls import path
from .views import register_user,send_message,sent_messages,received_messages

urlpatterns = [
    path('register/', register_user),
    path('send/',send_message),
    path('messages/received/<str:username>/',received_messages),
    path('messages/sent/<str:username>/',sent_messages)
]
