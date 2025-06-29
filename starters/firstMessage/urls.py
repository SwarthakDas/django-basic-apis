from django.urls import path
from .views import send_hey,register_user

urlpatterns = [
    path('hey/',send_hey),
    path('register/', register_user),
]
