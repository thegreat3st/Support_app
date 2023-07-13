from django.db import models
from django.conf import settings
from src.tickets.constants import TicketStatus


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    
    def __str__(self):
       return self.name

class Ticket(models.Model):

    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    visibility = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField(default=TicketStatus.NOT_STARTED)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="user_tickets",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="manager_tickets",
        null=True,
    )

    class Meta:
        db_table = "tickets"
