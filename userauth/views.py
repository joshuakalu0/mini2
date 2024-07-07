
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from userauth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate





# Serializers
from userauth.serializer import MyTokenObtainPairSerializer,UserSerializer,RegisterSerializer,UserLoginSerializer

from organisation.models  import Organisation



class MyTokenObtainPairView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request=request,email=email,password=password)
        if user:
            token = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                      "accessToken":str(token.access_token),
                    "user": {
                         "userId": user.userId,
                         "firstName": user.firstName,
                         "lastName": user.lastName,
                         "email": user.email,
                         "phone": user.phone,
                         }
                    }
                },status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            },status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        statu =  self.create(request, *args, **kwargs)
        if statu.status_code == 201:
            user = User.objects.get(email = request.data['email'])
            token = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                      "accessToken":str(token.access_token),
                    "user": {
                         "userId": user.userId,
                         "firstName": user.firstName,
                         "lastName": user.lastName,
                         "email": user.email,
                         "phone": user.phone,
                         }
                    }
                },status=status.HTTP_201_CREATED)


        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
            },status=status.HTTP_400_BAD_REQUEST)



