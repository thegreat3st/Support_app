from django.contrib import admin
from django.urls import path, include
from src.authentication.routers import CustomReadOnlyRouter
from src.authentication.views import UserViewSet # MyObtainTokenPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = CustomReadOnlyRouter()
router.register('', UserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title="Support API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('', include('trash.pokemons')), POKEMONS LINK
    path('auth/', include('src.authentication.urls')),
    path('tickets/', include('src.tickets.urls')),
    path('', include(router.urls)),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

