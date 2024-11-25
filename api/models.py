from django.db import models
from django.conf import settings

# Create your models here.

class Scene(models.Model):
    name = models.CharField(max_length=255, default="")
    url_background = models.CharField(max_length=255, default="", null=True)
    url_text_box = models.CharField(max_length=255, default="", null=True)
    url_character_left = models.CharField(max_length=255, default="", null=True)
    url_character_middle = models.CharField(max_length=255, default="", null=True)
    url_character_right = models.CharField(max_length=255, default="", null=True)
    text = models.CharField(max_length=255, default="", null=True)

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name="project")
    name = models.CharField(max_length=255)
    privacy = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_scene = models.OneToOneField(Scene, default='',on_delete=models.CASCADE)

class Choice(models.Model):
    text = models.CharField(max_length=255, default="")
    from_scene = models.ForeignKey(Scene, default='', on_delete=models.CASCADE, related_name='from_scene')
    to_scene = models.OneToOneField(Scene, null=True, on_delete=models.CASCADE, related_name='to_scene')