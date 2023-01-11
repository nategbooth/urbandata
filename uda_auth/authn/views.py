from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .forms import CreateUserForm
from .serializers import UserSerializer
from .models import CustomAuthUser


def create_user(request):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all users.
    """
    queryset = CustomAuthUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
