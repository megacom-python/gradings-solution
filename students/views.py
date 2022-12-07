from rest_framework import generics
from students.serializers import RegisterUserSerializer, ObtainTokenSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer


class ObtainTokenAPIView(generics.CreateAPIView):
    serializer_class = ObtainTokenSerializer
