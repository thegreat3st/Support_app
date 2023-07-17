from tickets.models import Ticket

from django.contrib.auth import get_user_model

User = get_user_model()


# *****************************************************
# Function implementation
# *****************************************************
# def assign_to_manager(user: User, ticket: Ticket) -> Ticket:
#     ticket.manager = user
#     ticket.save()

#     return ticket


# *****************************************************
# Class implementation
# *****************************************************
class AssignService:
    def __init__(self, ticket: Ticket):
        self._ticket = ticket

    def assign_manager(self, user: User):
        self._ticket.manager = user
        self._ticket.save()