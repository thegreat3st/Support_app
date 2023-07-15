from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, status
from src.tickets.models import Ticket, Category
from src.tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from src.tickets.serializers import (CategorySerializer, TicketAssignSerializer,
                                 TicketSerializer)

User = get_user_model()

    
class TicketAPIViewSet(ModelViewSet):
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

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
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def take(self, request, pk):
        ticket = self.get_object()
        # if (ticket == 0):

        # *****************************************************
        # Custom services approach
        # *****************************************************
        # updated_ticket: Ticket = AssignService(ticket).assign_manager(
        #     request.user,
        # )
        # serializer = self.get_serializer(ticket)

        # *****************************************************
        # Serializers approach
        # *****************************************************
        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        if (ticket.manager is None):
            ticket = serializer.assign(ticket)
            return Response(TicketSerializer(ticket).data)
        else:
            return Response(data={"Error 404, ticket is already taken"}, status=status.HTTP_404_NOT_FOUND)
        

    @action(detail=True, methods=["post"])
    def reassign(self, request, pk):
        ticket = self.get_object()
        serializer = TicketAssignSerializer(data={"manager_id": request.user.id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    