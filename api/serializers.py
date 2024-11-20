from rest_framework import serializers
from .models import Choice, Project, Scene
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtém o modelo de usuário real definido em settings.AUTH_USER_MODEL

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Define o modelo de usuário
        fields = ('id', 'username', 'password')  
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Garante que a senha será armazenada com hash
        user.save()
        return user

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
