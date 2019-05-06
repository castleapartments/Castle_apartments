from django.db import models

# Create your models here.
class Image(models.Model):
    imageID = models.AutoField(primary_key=True)
    imageURL = models.CharField(max_length=50)
    imageCreated = models.DateTimeField(auto_now_add=True)