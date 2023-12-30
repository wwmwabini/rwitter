import os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from rwitter.functions import random_image_name

default_post_image_folder='media/images/post_pics'

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    searchterm = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='post_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post #{self.id} by {self.user.username}' 
    
    def get_absolute_url(self):
        return reverse('tweets-home')
    
    
    

