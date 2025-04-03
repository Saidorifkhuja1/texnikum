from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'