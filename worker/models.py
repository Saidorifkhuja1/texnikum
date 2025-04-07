import uuid

from django.db import models

class Worker(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='worker/' )
    body = models.TextField()

    def __str__(self):
        return self.name

