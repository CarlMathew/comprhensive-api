from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status, permissions
from .models import Users
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate

# Create your views here.



class CreateUserAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = self.request.data.get("username")
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        role = self.request.data.get("role", "user")
        if not username or not password:
            return Response({"error": "Please provide a username and password"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(username=username).exists():
            return Response({"error" :"Username already exists"}, status = status.HTTP_400_BAD_REQUEST)
        
        if role not in ["admin", "manager", "user"]:
            return Response({"error": "Invalid Role"})
        

        try:
            new_user = Users.objects.create_user(username = username, email = email, password = password, role = role)
            return Response({"message" : f"User: {username} is now created"}, status = status.HTTP_201_CREATED)
        except Exception as e: 
            return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username = username, password = password)

        if user is None:
            return Response ({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)