from django.db import models

# 
class Container(models.Model):
    container_name = models.CharField(max_length=130)
    container_text = models.TextField()

    CONTAINER_CHOICES = (
            ('frontend',    'Frontend'),
            ('footer',   'Footer'),
        )

    container_location = models.CharField(
        max_length=20,
        choices=CONTAINER_CHOICES,
        default='footer')

    def __str__(self):
        return str(self.container_name)