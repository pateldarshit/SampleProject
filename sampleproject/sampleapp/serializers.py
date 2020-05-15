from django.contrib.auth.models import User
from rest_framework import serializers

from .constants import ContentType
from .models import ManifestoItem


class ManifestoItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = ManifestoItem
        fields = ["id", "title", "description", "content_type", "owner"]


class UserSerializer(serializers.ModelSerializer):
    manifesto_items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ManifestoItem.objects.all()
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "items",
        ]
