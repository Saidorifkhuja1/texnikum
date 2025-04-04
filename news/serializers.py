from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = News
        fields = ['uid','title', 'body', 'image']
