from rest_framework import serializers
from .models import Worker



class WorkerSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Worker
        fields = '__all__'

