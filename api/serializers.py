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
    first_scene = serializers.PrimaryKeyRelatedField(queryset=Scene.objects.all(), required=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'privacy', 'created_at', 'updated_at', 'first_scene']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        return super().create(validated_data)
    
    def validate_first_scene(self, value):
        # Verifica se a cena existe, mesmo que já seja um PrimaryKeyRelatedField
        if not Scene.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Cena não encontrada")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome do projeto não pode estar vazio.")
        return value

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'name', 'url_background', 'url_text_box', 'url_character_left', 'url_character_middle', 'url_character_right', 'text')

class ChoiceSerializer(serializers.ModelSerializer):
    from_scene = serializers.PrimaryKeyRelatedField(queryset=Scene.objects.all(), required=True)
    to_scene = serializers.PrimaryKeyRelatedField(queryset=Scene.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Choice
        fields = ['id', 'text', 'from_scene', 'to_scene']
        read_only_fields = ['id']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate_from_scene(self, value):
        # Valida se a cena de origem existe
        if not Scene.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("A cena de origem não foi encontrada.")
        return value

    def validate_to_scene(self, value):
        # Valida se a cena de destino existe, se fornecida
        if value and not Scene.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("A cena de destino não foi encontrada.")
        return value

    def validate_text(self, value):
        # Verifica se o texto não está vazio ou apenas com espaços
        if not value.strip():
            raise serializers.ValidationError("O texto da escolha não pode estar vazio.")
        return value
