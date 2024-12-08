from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import serializers
from .serializers import ProjectSerializer, SceneSerializer, ChoiceSerializer, UserSerializer
from .models import Project, Scene, Choice
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

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

class ProjectViewSetWithID(viewsets.ModelViewSet): #Para endpoint
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de um projeto específico com base no ID fornecido.
        """
        # Obtém o objeto filtrando pelo ID e pelo usuário autenticado
        queryset = self.get_queryset()
        project = queryset.filter(id=kwargs['pk']).first()

        if not project:
            return Response({"detail": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(project)
        return Response(serializer.data)
    
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
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        # Retorna apenas os projetos do usuário autenticado
        return Project.objects.filter(user=self.request.user)

class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        project_id = self.request.query_params.get('id')
        if not project_id:
            raise NotFound("O parâmetro 'id' é obrigatório.")
        return get_object_or_404(self.queryset, id=project_id)

    def get_queryset(self):
        # Retorna apenas os projetos pertencentes ao usuário autenticado
        return Project.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Garantir que o projeto pertence ao usuário autenticado
        project = self.get_object()
        if project.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para modificar este projeto.")

        # Pega o ID da nova cena (first_scene) caso seja passado no request
        first_scene_id = self.request.data.get('first_scene')

        # Verifica se o ID foi passado e se a cena existe
        if first_scene_id:
            first_scene = Scene.objects.get(id=first_scene_id)
            serializer.save(first_scene=first_scene)
        else:
            # Se o campo first_scene não for passado, apenas atualiza o projeto
            serializer.save()

class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('id')
        
        try:
            # Usar 'user' no lugar de 'owner'
            project = Project.objects.get(id=project_id, user=request.user)  # Altere 'owner' para 'user'
            project.delete()  # Deletar o projeto
            return Response(status=status.HTTP_204_NO_CONTENT)  # Retornar sucesso
        except Project.DoesNotExist:
            return Response({'detail': 'Projeto não encontrado ou você não tem permissão para deletá-lo.'}, 
                            status=status.HTTP_404_NOT_FOUND)


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
    def patch(self, request, *args, **kwargs):
        scene_id = request.query_params.get('id')  # Pega o 'id' da query string
        if not scene_id:
            return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scene = Scene.objects.get(id=scene_id)
            # Atualize os campos com os dados recebidos no request.data
            for attr, value in request.data.items():
                setattr(scene, attr, value)
            scene.save()

            # Serializa a instância de 'scene' para o formato JSON
            serializer = SceneSerializer(scene)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Scene.DoesNotExist:
            return Response({'error': 'Cena não encontrada'}, status=status.HTTP_404_NOT_FOUND)

class SceneDeleteView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        scene_id = request.query_params.get('id')  # Pega o 'id' da query string
        if not scene_id:
            return JsonResponse({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scene = Scene.objects.get(id=scene_id)
            scene.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Scene.DoesNotExist:
            return JsonResponse({'error': 'Cena não encontrada'}, status=status.HTTP_404_NOT_FOUND)

# Choice

# Choice
class ChoiceViewSet(viewsets.ModelViewSet):  # Para endpoints REST completos (CRUD)
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

class ChoiceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceCreateView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        # Apenas salva o objeto sem restrições adicionais
        serializer.save()

class ChoiceListView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Choice
from .serializers import ChoiceSerializer

class ChoiceUpdateView(generics.UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        choice_id = request.query_params.get('id')  # Pega o 'id' da query string
        if not choice_id:
            return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            choice = Choice.objects.get(id=choice_id)

            # Atualiza os campos com os dados recebidos no request.data
            for attr, value in request.data.items():
                if attr == "from_scene" or attr == "to_scene":
                    # Se o campo for um relacionamento (como 'from_scene' ou 'to_scene'), busque a instância
                    try:
                        value = Scene.objects.get(id=value)  # Obtém a instância de Scene com o ID fornecido
                    except Scene.DoesNotExist:
                        return Response({'error': f"Cena com ID {value} não encontrada."}, status=status.HTTP_404_NOT_FOUND)
                
                setattr(choice, attr, value)  # Atribui o valor ao campo da escolha

            choice.save()

            # Serializa a instância de 'choice' para o formato JSON
            serializer = ChoiceSerializer(choice)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Choice.DoesNotExist:
            return Response({'error': 'Escolha não encontrada'}, status=status.HTTP_404_NOT_FOUND)

class ChoiceDeleteView(generics.DestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def delete(self, request, *args, **kwargs):
        choice_id = request.query_params.get('id')  # Pega o 'id' da query string
        if not choice_id:
            return JsonResponse({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            choice = Choice.objects.get(id=choice_id)
            choice.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Choice.DoesNotExist:
            return JsonResponse({'error': 'Escolha não encontrada'}, status=status.HTTP_404_NOT_FOUND)