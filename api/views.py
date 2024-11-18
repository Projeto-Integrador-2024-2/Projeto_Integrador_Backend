from django.shortcuts import render
from rest_framework import generics
from .serializers import ProjectSerializer, SceneSerializer, ChoiceSerializer
from .models import Project, Scene, Choice

# Create your views here.
# generics.ListAPIView (Para ver)
# generics.CreateAPIView (Para Criar)

class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class SceneView(generics.ListAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

class ChoiceView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer