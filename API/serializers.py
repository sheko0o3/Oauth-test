from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Book

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "id" )



class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    
    class Meta:
        model = Book
        fields = ("name", "author")