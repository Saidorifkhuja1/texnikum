import uuid
from django.utils import timezone
from django.db import models



class Comment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=500)
    family_name = models.TextField(max_length=500)
    body = models.TextField()
    phone = models.CharField(max_length=250)


    def __str__(self):
        return self.name
