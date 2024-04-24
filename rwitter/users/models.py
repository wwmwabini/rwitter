
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

default_profile_image_folder = 'media/images/profile_pics'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=512, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.user.email}' 
    
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
    

