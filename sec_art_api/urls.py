from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sec_art_api.storage.views import StorageViewSet
from sec_art_api.user.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'groups', viewset=GroupViewSet)
router.register(r'storage', viewset=StorageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("admin/", admin.site.urls),
]
