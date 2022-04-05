from .models import url
from rest_framework import serializers


class urlSerializer(serializers.ModelSerializer):
    class Meta:
        model = url
        fields = "__all__"
