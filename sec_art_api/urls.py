from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("storage/", include("sec_art_api.storage.urls")),
    path('admin/', admin.site.urls),
]
