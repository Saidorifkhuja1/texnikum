from rest_framework import serializers
from .models import Slide

class SlideSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Slide
        fields = ['uid','title', 'body', 'image']
