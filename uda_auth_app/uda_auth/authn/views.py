from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import  Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

from authn.serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


