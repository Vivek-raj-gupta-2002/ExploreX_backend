from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.GoodBad)
admin.site.register(models.Notes)
admin.site.register(models.Post)