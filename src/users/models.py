from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from src.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    role = models.PositiveSmallIntegerField()

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.email
        
class Request(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    visibility = models.BooleanField()
    status = models.PositiveSmallIntegerField ()
    user = models.ForeignKey (User, on_delete=models .RESTRICT, related_name="user_requests")
    manager = models.ForeignKey (User, on_delete=models .RESTRICT, related_name="manager_requests")
    
    class Meta():
        db_table = "requests"    
    
class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="messages")
    request = models.ForeignKey(Request, on_delete=models.RESTRICT, related_name="messages")
    
    class Meta():
        db_table = "messages"