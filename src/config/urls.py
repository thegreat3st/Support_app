from django.contrib import admin
from django.urls import path, include
from src.authentication.routers import CustomReadOnlyRouter
from src.authentication.views import UserViewSet# , MyObtainTokenPairView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView


router = CustomReadOnlyRouter()
router.register(r'user', UserViewSet, basename='User')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", include("src.users.api")),
    path('', include('trash.pokemons')),
    # path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('src.authentication.urls')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

