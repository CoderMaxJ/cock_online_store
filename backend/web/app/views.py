from django.shortcuts import render
from rest_framework.views import APIView
from .models import Cocks
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import  AllowAny,IsAuthenticated
from rest_framework import  status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . serializers import AccountSerializer, PostsSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAccount(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # if your serializer supports commit=False
            # Hash the password
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self,request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                print("success")
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = Response({'status':'login successful'}, status=status.HTTP_200_OK)

                response.set_cookie(
                    key="access_token",
                    value=access_token,  # JWT token
                    httponly=True,  # prevents JS access (secure)
                    secure=False,  # True if HTTPS
                    samesite="Lax"
                )

                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=False,
                    samesite="Lax"
                )
                return response

            else:
                return Response({"message":"Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error":"username and password are required"},status=status.HTTP_400_BAD_REQUEST)

class UploadView(APIView):

    def post(self,request):
        print(request.data)
        if request.user.is_authenticated:
            owner = request.user
        else:
            # fallback: choose an existing test user (create one in admin or via manage.py)
            owner = User.objects.filter(is_superuser=True).first()
        bloodline = request.data.get('bloodline')
        price = request.data.get('price')
        images = request.FILES.getlist('images')
        image1 = images[0] if len(images) > 0 else None
        image2 = images[1] if len(images) > 1 else None
        image3 = images[2] if len(images) > 2 else None
        broodcock = images[3] if len(images) > 3 else None
        broodhen = images[4] if len(images) > 4 else None

        image_list = []

        cock = Cocks(
                       bloodline = bloodline,
                       image1=image1,
                       image2=image2,
                       image3=image3,
                       broodcock=broodcock,
                       broodhen=broodhen,
                       owner=owner,
                       price=price)
        if cock:
            cock.save()
        print(image_list)
        return Response({"message":"images uploaded successfully"},status=status.HTTP_200_OK)

class Posts(APIView):

    def get(self,request):
        posts = Cocks.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)
