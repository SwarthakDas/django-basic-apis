from django.urls import path
from .views import register_user,send_message,sent_messages,received_messages,login_user,logout_user

urlpatterns = [
    path('register/', register_user),
    path('send/',send_message),
    path('login/',login_user),
    path('logout/',logout_user),
    path('messages/received/<str:username>/',received_messages),
    path('messages/sent/<str:username>/',sent_messages)
]
