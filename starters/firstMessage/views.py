from django.http import JsonResponse
import json
from .models import User,Messages
from django.views.decorators.csrf import csrf_exempt

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