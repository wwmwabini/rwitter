from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    searchterm = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)