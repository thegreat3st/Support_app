from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.config.celery import celery_app
from src.tickets.models import Ticket, Category, Message
from src.tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from src.tickets.serializers import (CategorySerializer, TicketAssignSerializer,
                                     TicketSerializer, MessageSerializer)
from src.users.user_constants import Role
from time import sleep

User = get_user_model()

    
@celery_app.task
def send_email():
    print("📭 Sending email")
    sleep(10)
    print("✅ Email sent")

    
class TicketAPIViewSet(ModelViewSet):
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        all_tickets = Ticket.objects.all()

        if user.role == Role.ADMIN:
            return all_tickets
        elif user.role == Role.MANAGER:
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        else:
            # User's role fallback solution
            return all_tickets.filter(user=user)

    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
        elif self.action == "create":
            permission_classes = [RoleIsUser]
        elif self.action == "retrieve":
            permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
        elif self.action == "update":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "destroy":
            permission_classes = [RoleIsAdmin | RoleIsManager]
        elif self.action == "take":
            permission_classes = [RoleIsManager]
        elif self.action == "reasign":
            permission_classes = [RoleIsAdmin]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["PUT"])
    def take(self, request, pk):
        ticket = self.get_object()

        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        if (ticket.manager is None):
            ticket = serializer.assign(ticket)
            if ticket.manager_id is not None:
                return Response(TicketSerializer(ticket).data)
            else:
                return Response(data={"Error 403, manager has more than 2 tickets pending!"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={"Error 404, ticket is already taken"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["PUT"])
    def reasign(self, request, pk): 
        ticket = self.get_object()
        
        serializer = TicketAssignSerializer(data=request.data)
        serializer.is_valid()
        if (request.user.is_superuser is True):
            ticket = serializer.assign(ticket)
            if ticket.manager_id is not None:
                return Response(TicketSerializer(ticket).data)
            else:
                return Response(data={"Error 403, manager has more than 3 tickets pending!"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={"Error 403, only admin can reasign!"}, status=status.HTTP_403_FORBIDDEN)
        
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class MessageListCreateAPIView(ListCreateAPIView):
    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        # ticket = get_object_or_404(
        #     Ticket.objects.all(), id=self.kwargs[self.lookup_field]
        # )
        # if ticket.user != self.request.user and ticket.manager != self.request.user:
        #     raise Http404

        return Message.objects.filter(
            Q(ticket__user=self.request.user) | Q(ticket__manager=self.request.user),
            ticket_id=self.kwargs[self.lookup_field],
        )

    @staticmethod
    def get_ticket(user: User, ticket_id: int) -> Ticket:
        """Get tickets for current user."""

        tickets = Ticket.objects.filter(Q(user=user) | Q(manager=user))
        return get_object_or_404(tickets, id=ticket_id)

    def post(self, request, ticket_id: int):
        ticket = self.get_ticket(request.user, ticket_id)
        payload = {
            "text": request.data["text"],
            "ticket": ticket.id,
        }
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
            # else:
            #     return Response(data={"Error 403, dont spam!"}, status=status.HTTP_403_FORBIDDEN)