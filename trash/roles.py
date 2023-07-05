from random import randint, choice
from django.http import HttpResponse

ROLES = {
    "ADMIN": 1,
    "MANAGER": 2,
    "USER": 3,
}


def _get_random_string(size: int = 5) -> str:
    return "".join([choice(ascii_letters) for _ in range(size)])


def create_random_user(request):
    email_prefix = _get_random_string(size=randint(5, 8))
    email_affix = _get_random_string(size=randint(2, 5))
    email = "".join((email_prefix, "@", email_affix, ".com"))

    user = User.objects.create(
        username=_get_random_string(size=randint(5, 10)),
        email=email,
        first_name=_get_random_string(size=randint(5, 10)),
        last_name=_get_random_string(size=randint(5, 10)),
        password=_get_random_string(size=randint(10, 20)),
        role=ROLES["USER"],
    )

    result = {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "role": user.role,
    }

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


urlpatterns = [
    path("create-random-user", create_random_user),
]