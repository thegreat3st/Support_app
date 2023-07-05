from src.core.models import User
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from random import choice, randint
from string import ascii_letters
from src.users.user_constants import ROLES
import json

def _get_random_string(size: int = 5) -> str:
    return "".join([choice(ascii_letters) for _ in range(size)])

def create_random_user(request):
    username= _get_random_string(size=randint(5,10))
    user = User.objects.create(
        username= "".join([i for i in ROLES if ROLES[i]==3]) + "_" + username,
        email= "".join((username, "@", _get_random_string(size=randint(2, 5)), ".com")),
        first_name=_get_random_string(size=randint(5,10)),
        last_name=_get_random_string(size=randint(5,10)),
        password=_get_random_string(size=randint(10,20)),
        role= 3
    )
    result = {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "password": user.password,
        "role": user.role,
    }
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )
    
urlpatterns = [
    path("create-random-user/", create_random_user)
]