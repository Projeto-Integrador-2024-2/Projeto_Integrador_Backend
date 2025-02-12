from rest_framework import serializers
from .models import Choice, Project, Scene, Genre, Description, Grade
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtém o modelo de usuário real definido em settings.AUTH_USER_MODEL

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Define o modelo de usuário
        fields = ('id', 'username', 'password', 'email', 'is_staff')
        read_only_fields = ['is_staff']  
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Garante que a senha será armazenada com hash
        user.save()
        return user
    
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'name', 'url_background', 'url_text_box', 'url_character_left', 'url_character_middle', 'url_character_right', 'text', 'project')

class ProjectSerializer(serializers.ModelSerializer):
    first_scene = SceneSerializer(read_only=True)  # Somente leitura
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)  # Ajuste para ManyToMany
    average_grade = serializers.SerializerMethodField()  # Adicionando o campo corretamente

    class Meta: 
        model = Project
        fields = ['id', 'name', 'privacy', 'created_at', 'updated_at', 'first_scene', 'genres', 'average_grade']
        read_only_fields = ['id', 'created_at', 'updated_at', 'first_scene', 'average_grade']
    
    def validate_first_scene(self, value):
        # Supondo que o valor seja um dict
        if isinstance(value, dict):  # Verifica se value é um dict
            scene_id = value.get('id', None)  # Use .get() para evitar erros
            if scene_id is None:
                raise serializers.ValidationError("ID não encontrado.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome do projeto não pode estar vazio.")
        return value
    
    def get_average_grade(self, obj):
        #print(f"#{obj.id} : ", Grade.objects.filter(project=obj))
        #print(f"Aggregate Result: {average_query}")
        average_query = Grade.objects.filter(project=obj).exclude(grade_value__isnull=True).filter(grade_value__gte=0).aggregate(Avg('grade_value'))
        average = Grade.objects.filter(project=obj).aggregate(Avg('grade_value'))['grade_value__avg']
        return round(average, 2) if average is not None else 0.0
    
class ProjectSerializerUpdate(serializers.ModelSerializer):
    first_scene = serializers.PrimaryKeyRelatedField(queryset=Scene.objects.all(), required=False)
    name = serializers.CharField(required=False)  # Não obrigatório
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, required=False)  # Ajuste para ManyToMany

    class Meta:
        model = Project
        fields = ['id', 'name', 'privacy', 'created_at', 'updated_at', 'first_scene', 'genres']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_first_scene(self, value):
        if isinstance(value, dict):  # Verifica se value é um dict
            scene_id = value.get('id', None)  # Usa .get() para evitar erros
            if scene_id is None:
                raise serializers.ValidationError("ID não encontrado.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome do projeto não pode estar vazio.")
        return value

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

class DescriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Permite associar a um usuário
    description = serializers.CharField(max_length=500)  # Tamanho da descrição ajustável

    class Meta:
        model = Description
        fields = ['user', 'description']

    def create(self, validated_data):
        return Description.objects.create(**validated_data)

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("A descrição não pode estar vazia.")
        return value
    
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'user', 'project', 'grade_value', 'feedback']