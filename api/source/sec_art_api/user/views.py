import logging
import os
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.http import FileResponse, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from sec_art_api.settings import (
    EMAIL_SENDER,
    USER_ACTIVATION_TOKEN_EXPIRED_DAYS,
    HOST_NAME,
    MEDIA_ROOT,
)
from .models import UserActivationToken

from sec_art_api.user.models import User, UserActivationToken
from sec_art_api.user.serializers import (
    GroupSerializer,
    UserActivationTokenSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateUserViewSet(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _send_activation_email(self, user: User):
        logger = logging.getLogger("ir-server-api")
        expired_at = datetime.now() + timedelta(USER_ACTIVATION_TOKEN_EXPIRED_DAYS)
        user_id = user.id
        serializer = UserActivationTokenSerializer(
            data={"user_id": user_id, "expired_at": expired_at}
        )
        serializer.is_valid(raise_exception=True)
        user_activation_token = serializer.save()
        user_email = user.email
        token = user_activation_token.token
        subject = "アカウント認証のお願い"
        message = f"以下のリンクをクリックしてメールアドレスの認証を行ってください\n {HOST_NAME}/user/activate/{token}"
        send_mail(
            from_email=EMAIL_SENDER,
            recipient_list=[user_email],
            subject=subject,
            message=message,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        self._send_activation_email(user)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


def activate_user(request, activate_token):
    activated_user = UserActivationToken.objects.activate_user(activate_token)
    if hasattr(activated_user, "is_active"):
        if activated_user.is_active:
            message = "ユーザーのアクティベーションが完了しました"
        if not activated_user.is_active:
            message = "アクティベーションが失敗しています。管理者に問い合わせてください"
    if not hasattr(activated_user, "is_active"):
        message = "エラーが発生しました"
    return HttpResponse(message)
