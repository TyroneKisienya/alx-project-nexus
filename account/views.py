from django.shortcuts import render
from .serializers import RegisterSerializer, Userserializers, ProfileUpdateSerializer
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()
class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProfileViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        serializer = Userserializers(request.user, context = {"request": request})
        return Response(serializer.data)
    
    @action(detail=False, methods=["patch"], url_path="me")
    def partial_update_me(self, request):
        serializer = ProfileUpdateSerializer(request.user, data = request.data, partial = True, context = {"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        out = Userserializers(user, context = {"request": request}).data
        return Response(out, status=status.HTTP_200_OK)