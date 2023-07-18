from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.tickets.models import Ticket, Category
from src.tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from src.tickets.serializers import (CategorySerializer, TicketAssignSerializer,
                                     TicketSerializer)
from src.users.user_constants import Role

User = get_user_model()

    
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
                return Response(data={"Error 403, manager has more than 3 tickets pending!"}, status=status.HTTP_403_FORBIDDEN)
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
    