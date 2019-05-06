from django.db import models


# Create your models here.
class Image(models.Model):
    imageID = models.AutoField(primary_key=True)
    imageURL = models.ImageField(upload_to="media/", blank=True, unique=True)
    imageCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.imageURL)