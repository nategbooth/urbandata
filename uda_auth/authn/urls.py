from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('users/create', views.create_user, name='create_user'),
    path('authn/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authn/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
