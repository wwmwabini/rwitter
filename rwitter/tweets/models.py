import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, ValidationError
from django.urls import reverse
from PIL import Image
from rwitter.functions import random_image_name


default_post_image_folder='media/images/post_pics'
default_feedback_media_folder='media/feedback_media'

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    searchterm = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    content = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='post_media')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post #{self.id} by {self.user.username}'

    @property
    def post_comments(self):
        return Comment.objects.filter(post=self) 

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    def get_absolute_url(self):
        return reverse('tweets-home')
    

class Comment(models.Model):
    content = models.TextField(max_length=180, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on post {self.post.id}'
    




class Feedback(models.Model):
    
    class Subject(models.TextChoices):
        provide_recommendation = 'Provide Recommendation'
        error_experienced = 'Error Experienced'
        report_abuse = 'Report Abuse'
        other = 'Other'
    subject = models.CharField('What is it About?', max_length=25, choices=Subject.choices)
    content = models.TextField('Tell us more', max_length=2500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField('Upload an image or video(recommended)', upload_to='feedback_media/', null=True, blank=True, 
                             validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', 'gif', 'mov', 'mp4', 'mp3', 'mkv'])])

    def __str__(self):
        return f'#{self.id} Feedback shared by {self.user.username} on {self.created_at.strftime("%d %B, %Y %H:%M")}'
    

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    story = models.ImageField('Tell your story with an image or video', blank=True, null=True, upload_to='stories_media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story #{self.id} by {self.user.username}'
    
    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"
