from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta, datetime
from rwitter.functions import handle_uploaded_file


class Ads(models.Model):
    message = models.CharField(max_length=40)
    image = models.ImageField(upload_to='ads_media/', null=True, blank=True)
    redirect_website = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.id:
            self.end_date = datetime.today() + timedelta(days=15)
        
        media_location = 'ads_media'

        ads_file = handle_uploaded_file(self.image, media_location, 'ads')
        self.image = ads_file

        super().save()

    def __str__(self):
        return f'Ad #{self.id} by {self.owner.username}'
    
    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"

class AdClick(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "AdClick"
        verbose_name_plural = "AdClicks"

class AdReport(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "AdReport"
        verbose_name_plural = "AdReports"

class AdHide(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "AdHide"
        verbose_name_plural = "AdHides"