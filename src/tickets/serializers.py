from rest_framework import serializers
from src.tickets.models import Ticket, Category


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ["id","category", "title", "text", "visibility", "status", "user", "manager", "created"]
        read_only_fields = ["visibility", "manager", "created"]


class TicketAssignSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def validate_manager_id(self, manager_id):
        # ? You can handle the specific validation if
        # ? the manager already has 10 tickets assigned
        return manager_id

    def assign(self, ticket: Ticket) -> Ticket:
        ticket.manager_id = self.validated_data["manager_id"]
        ticket.save()

        return ticket

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')