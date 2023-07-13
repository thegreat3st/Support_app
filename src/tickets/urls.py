from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.tickets.views import TicketAPIViewSet, CategoryViewSet

router = DefaultRouter()
router.register('', TicketAPIViewSet, basename="tickets")
router.register('', CategoryViewSet, basename="category")

urlpatterns = router.urls + [
    path(r'', include(router.urls)),
    path(r'', include('rest_framework.urls', namespace='rest_framework'))
]