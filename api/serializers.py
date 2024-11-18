from rest_framework import serializers
from .models import Choice, Project, Scene

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'private', 'created_at', 'updated_at', 'first_scene')

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'name', 'url_background', 'url_text_box', 'url_character_left', 'url_character_middle', 'url_character_right', 'text')

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', 'from_scene', 'to_scene')
