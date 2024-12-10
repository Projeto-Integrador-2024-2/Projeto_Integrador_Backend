from django.contrib import admin
from .models import Project, Scene, Choice, Description

# Register your models here.
admin.site.register(Project)
admin.site.register(Scene)
admin.site.register(Choice)
admin.site.register(Description)