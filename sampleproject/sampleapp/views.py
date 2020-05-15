# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers

from .models import ManifestoItem
from .serializers import ManifestoItemSerializer, UserSerializer
from rest_framework import permissions


class ManifestoItemViewSet(viewsets.ModelViewSet):
    """
    Viewset for ManifestoItem
    """

    queryset = ManifestoItem.objects.all()
    serializer_class = ManifestoItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: serializers.Serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for Users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
