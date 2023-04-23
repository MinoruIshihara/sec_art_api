from rest_framework import viewsets
from rest_framework import permissions
from .models import Storage

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all().order_by('created')
#    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
