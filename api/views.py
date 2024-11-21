from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import serializers
from .serializers import ProjectSerializer, SceneSerializer, ChoiceSerializer, UserSerializer
from .models import Project, Scene, Choice
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# generics.CreateAPIView (Para Criar)
# generics.ListAPIView (Para ver)
# generics.UpdateAPIView (Para Updatar)
# generics.DeleteAPIView (Para Deletar)
# generics.RetrieveUpdateDestroyAPIView (Para Td)

# User

User = get_user_model()  # Obtém o modelo de usuário real definido em settings.AUTH_USER_MODEL

class UserView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserCreateView(generics.CreateAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserListView(generics.ListAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserUpdateView(generics.UpdateAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDeleteView(generics.DestroyAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Project

class ProjectViewSet(viewsets.ModelViewSet): #Para endpoint
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        # Retorna apenas os projetos do usuário autenticado
        return Project.objects.filter(user=self.request.user)

class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados possam acessar

    def perform_create(self, serializer):
        # Atribui o usuário logado ao projeto
        user = self.request.user
        # Garantir que o campo first_scene seja corretamente atribuído
        first_scene_id = self.request.data.get('firstScene')  # Pega o ID da cena
        if first_scene_id:
            first_scene = Scene.objects.get(id=first_scene_id)  # Obtém a cena pelo ID
            serializer.save(user=user, first_scene=first_scene)  # Atribui a cena ao projeto
        else:
            # Se first_scene não for passado, lance uma exceção ou defina um valor padrão
            raise serializers.ValidationError("A cena inicial é obrigatória.")

class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # Atribui o usuário logado ao projeto
        user = self.request.user
        # Garantir que o 'first_scene' seja corretamente mapeado
        first_scene = serializer.validated_data.get('first_scene')  # Pega o ID da cena validado
        serializer.save(user=user, first_scene=first_scene)

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# Scenes

class SceneViewSet(viewsets.ModelViewSet): #Para endpoint
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()

class SceneView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class SceneCreateView(generics.CreateAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class SceneListView(generics.ListAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class SceneUpdateView(generics.UpdateAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class SceneDeleteView(generics.DestroyAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

# Choice

class ChoiceViewSet(viewsets.ModelViewSet): #Para endpoint
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

class ChoiceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceCreateView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceListView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceUpdateView(generics.UpdateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceDeleteView(generics.DestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

#
