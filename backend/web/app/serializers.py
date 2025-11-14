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