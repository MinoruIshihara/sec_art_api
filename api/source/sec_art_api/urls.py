from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sec_art_api.storage.views import StorageViewSet
from django.http import HttpResponseNotFound


def root_not_found(request):
    return HttpResponseNotFound()


storage_router = routers.DefaultRouter()
storage_router.register(r"storage", viewset=StorageViewSet)

urlpatterns = [
    path("", root_not_found),
    path("user/", include("sec_art_api.user.urls")),
    path("storage", include(storage_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
