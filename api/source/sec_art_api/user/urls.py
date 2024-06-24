from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sec_art_api.user.views import (
    UserViewSet,
    GroupViewSet,
    CreateUserViewSet,
    activate_user,
)

app_name = "user"
user_router = routers.DefaultRouter()
user_router.register(r"users", viewset=UserViewSet)
user_router.register(r"groups", viewset=GroupViewSet)
user_router.register(r"create", viewset=CreateUserViewSet, basename="auth")

urlpatterns = [
    path("", include(user_router.urls)),
    path("activate/<uuid:activate_token>", activate_user, name="users-activation"),
]
