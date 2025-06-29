from django.http import JsonResponse
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt

def send_hey(req):
    return JsonResponse({
        "message":"hey",
        "success":True
    },status=201)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        User.objects.create(username=username, password=password)

        return JsonResponse({"success": True, "message": "User saved"}, status=201)

    return JsonResponse({"success": False, "message": "Only POST allowed"}, status=405)