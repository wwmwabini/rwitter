from django.contrib import admin
from .models import  Ads, AdClick, AdReport, AdHide


admin.site.register(Ads)
admin.site.register(AdClick)
admin.site.register(AdReport)
admin.site.register(AdHide)
