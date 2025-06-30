from django.http import JsonResponse
import json, jwt, datetime
from .models import User,Messages
from django.views.decorators.csrf import csrf_exempt
import environ

env = environ.Env()
environ.Env.read_env()

@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "message": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

    access_payload = {
        "_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(env("ACCESS_EXPIRY")))
    }
    refresh_payload = {
        "_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(env("REFRESH_EXPIRY")))
    }

    access_token = jwt.encode(access_payload, env("ACCESS_TOKEN"), algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, env("REFRESH_TOKEN"), algorithm="HS256")

    res = JsonResponse({"success": True, "message": "Login successful"}, status=201)
    res.set_cookie("accessToken", access_token, httponly=True, samesite='none')
    res.set_cookie("refreshToken", refresh_token, httponly=True, samesite='none')
    return res

@csrf_exempt
def logout_user(request):
    res = JsonResponse({"success": True, "message": "Logged out"})
    res.delete_cookie("accessToken")
    res.delete_cookie("refreshToken")
    return res

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        User.objects.create(username=username, password=password)

        return JsonResponse({"success": True, "message": "User saved"}, status=201)

    return JsonResponse({"success": False, "message": "Only POST allowed"}, status=405)

@csrf_exempt
def send_message(request):
    if not request.user:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    if(request.method!='POST'):
        return JsonResponse({"success":False,"message":"Only POST allowed"},status=405)
    
    data=json.loads(request.body)
    sender_name=data.get('sender')
    receiver_name=data.get('receiver')
    text=data.get('message')

    try:
        sender=User.objects.get(username=sender_name)
        receiver=User.objects.get(username=receiver_name)
    except User.DoesNotExist:
        return JsonResponse({"success":False,"message":"User not found"},status=404)
    
    Messages.objects.create(sender=sender,receiver=receiver,message=text)
    return JsonResponse({"success":True,"message":"Message sent successfully"},status=201)

@csrf_exempt
def received_messages(request,username):
    if not request.user:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"success":False,"message":"User not found"},status=404)
    
    msgs=user.received_messages.all().order_by("-timestamp")
    data=[
        {
            "sender":m.sender.username,
            "message": m.message,
            "timestamp":m.timestamp.isoformat()
        }
        for m in msgs
    ]
    return JsonResponse({"success":True,"messages":data},status=200)

@csrf_exempt
def sent_messages(request,username):
    if not request.user:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=401)
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"success":False,"message":"User not found"},status=404)
    
    msgs=user.sent_messages.all().order_by("-timestamp")
    data=[
        {
            "receiver":m.receiver.username,
            "message": m.message,
            "timestamp":m.timestamp.isoformat()
        }
        for m in msgs
    ]
    return JsonResponse({"success":True,"messages":data},status=200)