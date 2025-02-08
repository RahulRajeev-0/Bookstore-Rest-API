from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSignUpSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

# user signup function 
class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(): # validating the data 
            serializer.save()
            return Response(
                {"message":"User registration successfull"}, 
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    
# user login function 
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data) # validating data 
        if serializer.is_valid(): 
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password) # checking the login data
            # if user authenticated sending access and refresh token to user 
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
        
        

