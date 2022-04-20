from django.contrib import admin
from .models import Profile, TaskData

admin.site.register(TaskData)
admin.site.register(Profile)