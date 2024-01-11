import secrets, os

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from rwitter.functions import random_photo_name

default_profile_image_folder = 'media/images/profile_pics'

"""
def random_photo_name(self):
    _, photo_extension = os.path.splitext(self.photo.path)
    photo_filename = secrets.token_hex(12) + photo_extension
    print("Random photo name", photo_filename)

    return photo_filename
"""


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
        photo_name = random_photo_name(self)
        photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), default_profile_image_folder, photo_name)
        
        img = Image.open(self.photo.path)

        
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(photo_path)
        else:
            img.save(photo_path)

        #user_profile = UserProfile.objects.get(user=self.user)
        #user_profile.photo = photo_name
        #user_profile.save() 
    

