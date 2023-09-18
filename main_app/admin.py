from django.contrib import admin
from .models import Project, Comment, Profile, Task

# Register your models here
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Task)

