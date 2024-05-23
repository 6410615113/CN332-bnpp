from django.contrib import admin
from .models import Task, TaskStatus, Video, Loop

# Register your models here.
admin.site.register(Task)
# admin.site.register(TaskStatus)
admin.site.register(Video)
admin.site.register(Loop)