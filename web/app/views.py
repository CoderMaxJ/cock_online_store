from django.shortcuts import render
from rest_framework.views import APIView
from .models import Cocks
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny,IsAuthenticated
from rest_framework import  status
from django.contrib.auth import authenticate
from . serializers import AccountSerializer, PostsSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class Index(APIView):
    def get(self,request):
        return render(request,'index.html')

class RegisterAccount(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return   Response({"refresh_token": refresh_token, "access_token": access_token}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error":"username and password are required"},status=status.HTTP_400_BAD_REQUEST)

class UploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        owner = request.user
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
        return Response({"message":"images uploaded successfully"},status=status.HTTP_200_OK)

class Posts(APIView):
    def get(self,request):
        q=request.query_params.get('q')
        if q:
            posts = Cocks.objects.filter(bloodline__icontains=q)
        else:
            posts = Cocks.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)

class PostsDetails(APIView):
    def get(self,request,pk):
        post = Cocks.objects.get(id=pk)
        serializer = PostsSerializer(post)
        return Response(serializer.data)

