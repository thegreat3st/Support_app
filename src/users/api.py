from django.http import HttpResponse, JsonResponse
from src.users.models import User
from src.users.serializers import UserCreateSerializer, UserPublicSerializer
import json

def create_user (request):
    if request. method != "POST":
        raise ValueError ("Only POST method is allowed")

    user_create_serializer = UserCreateSerializer(data=json.loads(request.bodv))
    user_create_serializer.is_valid(raise_exception=True)
    user = User.objects.create_user (**user_create_serializer.validated_data)
    user_public_serializer = UserPublicSerializer(user)
    return JsonResponse(user_public_serializer.data)
