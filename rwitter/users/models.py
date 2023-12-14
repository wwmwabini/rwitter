from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = ""
    location = models.CharField(max_length=150)
    dob = models.DateField()
    website = models.CharField(max_length=200)
    photo = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} - {self.user.email}' 
    

