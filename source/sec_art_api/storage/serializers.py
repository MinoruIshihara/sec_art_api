from .models import Storage
from rest_framework import serializers

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Storage
        fields = ['name', 'created']