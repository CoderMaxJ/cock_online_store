from rest_framework import serializers
from django.contrib.auth.models import  User
from . models import Cocks
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name','email','is_staff','is_active','is_superuser']

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocks
        fields = '__all__'

class PostsSerializerPartial(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    date_posted = serializers.DateTimeField(format="%b,%d,%Y", read_only=True)
    class Meta:
        model = Cocks
        fields = ['id','image1','price','bloodline','location','like','heart','age','victory','spar_link','category','owner_username','date_posted']