from django.shortcuts import render
from rest_framework.views import APIView
from .models import Cocks
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny,IsAuthenticated
from rest_framework import  status
from django.contrib.auth import authenticate
from . serializers import AccountSerializer, PostsSerializer,PostsSerializerPartial
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
        print(request.data)
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                return   Response({"refresh_token": refresh_token, "access_token": access_token,"user":user.username,"user_id":user.id}, status=status.HTTP_200_OK)
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
        category = request.data.get('category')
        age = request.data.get('age')
        location = request.data.get('location')
        victory = request.data.get('victory') or 0
        spar_link = request.data.get('spar_link')

        image1 = images[0] if len(images) > 0 else None
        image2 = images[1] if len(images) > 1 else None
        image3 = images[2] if len(images) > 2 else None
        broodcock = images[3] if len(images) > 3 else None
        broodhen = images[4] if len(images) > 4 else None

        cock = Cocks(
                       bloodline = bloodline,
                       image1=image1,
                       image2=image2,
                       image3=image3,
                       broodcock=broodcock,
                       broodhen=broodhen,
                       owner=owner,
                       price=price,
                       category=category,
                       age=age,
                       location=location,
                       victory=victory,
                       spar_link=spar_link
                    )
        if cock:
            cock.save()
        return Response({"message":"images uploaded successfully"},status=status.HTTP_200_OK)

class Posts(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        user = authenticate(username='guest', password='letmein4321')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        try:
            q=request.query_params.get('q')
            t=request.query_params.get('t')
            if q or t:
                posts = Cocks.objects.filter(bloodline__icontains=q,category=t)[:100]
            else:
                posts = Cocks.objects.all()[:100]
            serializer = PostsSerializerPartial(posts, many=True)
            return Response({"data":serializer.data,"temporary_token":access_token},status=status.HTTP_200_OK)
        except Cocks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostsDetails(APIView):
    def get(self,request,pk):
        post = Cocks.objects.get(id=pk)
        serializer = PostsSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

class React(APIView):
    def post(self,request):
        id = request.data.get('id')
        type = request.data.get('type')

        if id and type:
            cock=Cocks.objects.get(id=id)
            if type == 'heart':
                cock.heart+=1
            elif type == 'like':
                cock.like+= 1
            cock.save()
        return Response(request.data,status=status.HTTP_200_OK)

class Comment(APIView):
    def post(self,request,id,user_id):
        post = Comment.objects.get(id=id)
        comment = request.data.get('comment')
        if comment:
            post
