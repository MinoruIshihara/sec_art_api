import logging
from typing import Any, Dict

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sec_art_api.user.models import User, UserActivationToken


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserActivationTokenSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = UserActivationToken
        fields = ["user_id", "expired_at"]

    def create(self, validated_data: Dict[str, Any]) -> UserActivationToken:
        logger = logging.getLogger("ir-server-api")
        user_id = validated_data.get("user_id", None)

        if user_id is not None:
            validated_data["user"] = user_id
            del validated_data["user_id"]
        logger.error(validated_data["user"].id)

        return super().create(validated_data)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
