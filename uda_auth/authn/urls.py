from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



from . import views


urlpatterns = [
    path('users/', views.users, name='users'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('authn/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authn/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
