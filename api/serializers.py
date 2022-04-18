from attr import fields
from .models import Device, url
from rest_framework import serializers


class urlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = "__all__"
