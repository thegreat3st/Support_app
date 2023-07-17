from rest_framework import serializers
from src.tickets.models import Ticket, Category
import sqlite3
from rest_framework.response import Response
from rest_framework.exceptions import status

class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ["id", "category", "title", "text", "visibility", 
                  "status", "user", "manager", "created_at"]
        read_only_fields = ["visibility", "manager", "created_at"]

class TicketAssignSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()
    
    def validate_manager_id(self, manager_id):
        
        with sqlite3.connect(database= 'src/db.sqlite3') as con:
            cur = con.cursor()
            cur.execute(f"SELECT id FROM tickets where manager_id = {manager_id} GROUP BY manager_id HAVING COUNT(*) < 3")
            if cur.fetchone():
                return manager_id
        # ? You can handle the specific validation if
        # ? the manager already has 10 tickets assigned
        # return manager_id

    def assign(self, ticket: Ticket) -> Ticket:
        ticket.manager_id = self.validated_data["manager_id"]
        ticket.save()

        return ticket


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
          
