from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication


from django.contrib.auth.models import User, Group


from .serializers import (UserSerializer,GroupSerializer)

from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from oauth2_provider.models import AccessToken, Application
from django.core.exceptions import ObjectDoesNotExist

import requests

# Create the API views
class UserList(generics.ListCreateAPIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



class CreateUser(APIView):

    def get_token(self, request):
        name = request.data.get("username", None)
        password = request.data.get("password", None)
        scope = request.data.get("scope", None)

        body: dict = {
            "client_id":"zWimZUaxgkRNpYNSP4NBIt6LJd6sO9UXeAuoahnU",
            "client_secret":"tUwEaNKF8tWeTTPdRydLbSMKmQ2BeYezyYWmzmXr4lP8JcwFnF9JA29L1MH0t3cFSnz7Hk2N2ELMncUiaLHY8fe4fcJDgUoQIcdU9DpvLOW70szK4HYp6MZ8FSf9H1MI",
            "username": name,
            "password": password,
            "grant_type":"password",
            "scope": scope
        }

        response = requests.post(url="http://127.0.0.1:8000/api/o/token/", data=body)
        data:dict = response.json()
        access_token = data.get("access_token", None)
        return data

    def post(self, request):
        serializer_class = UserSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save(password=make_password(request.data["password"]))
            token = self.get_token(request=request)

            return Response(data={"data":serializer_class.data,
                                  "token":token}, status=status.HTTP_201_CREATED)
        return Response(data=serializer_class.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class Token(APIView):

    def get(self, request):
        try:
            user = User.objects.get(username=request.data["username"])
        except ObjectDoesNotExist:
            return Response(data={"msg": "not found"})
        
        serializer = UserSerializer(instance=user)
        
        try:
            token = AccessToken.objects.get(user=user.id)
            return Response(data={"name":serializer.data.get("username", None),
                            "token":token.token}, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response(data={"msg": "no token related to this user"}, status=status.HTTP_404_NOT_FOUND)
