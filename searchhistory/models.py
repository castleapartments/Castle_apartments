from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchHistory(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)
    searchHistoryID = models.AutoField(primary_key=True)
    searchValue = models.CharField(max_length=50)
    searchFilter = models.CharField(max_length=50)
    searchHistoryCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.searchValue