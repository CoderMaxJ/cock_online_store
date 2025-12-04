from rest_framework import serializers, status
from django.contrib.auth.models import  User
from . models import Cocks,Comments,Contacts
from rest_framework.response import Response


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'comment', 'date_posted']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'number', 'messenger_link']

class AccountSerializer(serializers.ModelSerializer):
    number = serializers.CharField(required=False, allow_blank=True)
    messenger_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username','password','first_name','last_name',
            'number','messenger_link'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        number = validated_data.pop('number', None)
        messenger_link = validated_data.pop('messenger_link', None)

        # Create the User
        user = User.objects.create_user(**validated_data)
        if number or messenger_link:
            Contacts.objects.create(
                user=user,
                number=number,
                messenger_link=messenger_link
            )

        return user



class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocks
        fields = '__all__'

class PostsSerializerPartial(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    date_posted = serializers.DateTimeField(format="%b,%d,%Y", read_only=True)
    totalcomment = serializers.IntegerField(source='comments.count', read_only=True)
    number = serializers.SerializerMethodField()
    messenger_link = serializers.SerializerMethodField()

    class Meta:
        model = Cocks
        fields = ['id','image1','price','bloodline','location','like','heart','age','victory','spar_link','category','owner_username','date_posted','totalcomment','number','messenger_link']

    def get_number(self, obj):
        contact = getattr(obj.owner, 'contacts_set', None)
        if contact:
            contact = contact.first()
            return contact.number if contact else None
        return None

    def get_messenger_link(self, obj):
        contact = getattr(obj.owner, 'contacts_set', None)
        if contact:
            contact = contact.first()
            return contact.messenger_link if contact else None
        return None


class CommentsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Comments
        fields = ['id', 'cock', 'user', 'username', 'comment', 'date_posted']