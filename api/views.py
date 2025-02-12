from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import serializers
from .serializers import ProjectSerializer, ProjectSerializerUpdate, SceneSerializer, ChoiceSerializer, UserSerializer, GenreSerializer, DescriptionSerializer, GradeSerializer
from .models import Project, Scene, Choice, Genre, Description, Grade
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Choice
from .serializers import ChoiceSerializer
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError

class NotFound(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = "Nenhum conteúdo encontrado."
    default_code = "no_content"


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
    """
    View para criar um novo usuário e automaticamente associar uma descrição.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        # Crie uma descrição automaticamente ao criar o usuário
        Description.objects.create(user_id=user.id, description="Descrição padrão.")

class UserListView(generics.ListAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CurrentUserView(generics.RetrieveAPIView): 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_object(self): 
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.query_params.get('id')
        if not user_id:
            raise NotFound("O parâmetro 'id' é obrigatório.")
        return get_object_or_404(self.queryset, id=user_id)

    def get_queryset(self):
        # Apenas permite ao usuário atualizar seu próprio perfil
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        user = self.get_object()
        if user != self.request.user:
            raise PermissionDenied("Você não tem permissão para modificar este usuário.")
        
        # Salva as alterações do usuário
        serializer.save()

        # Atualiza ou cria a descrição se incluída no payload
        description_text = self.request.data.get('description')
        if description_text is not None:
            description, created = Description.objects.update_or_create(
                user_id=user.id,
                defaults={'description': description_text},
            )

class UserDeleteView(generics.DestroyAPIView): 
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Genre

class GenreView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class GenreCreateView(generics.CreateAPIView): 
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class GenreListView(generics.ListAPIView): 
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class GenreUpdateView(generics.UpdateAPIView): 
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

class GenreDeleteView(generics.DestroyAPIView): 
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

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
        # Salva o projeto primeiro
        user = self.request.user
        project = serializer.save(user=user)

        # Cria a primeira cena associada ao projeto
        first_scene = Scene.objects.create(
            project=project,
            name="-",
            url_background="-",
            url_text_box="-",
            url_character_left="-",
            url_character_middle="-",
            url_character_right="-",
            text="-",
        )

        # Atualiza o campo first_scene do projeto com a cena criada
        project.first_scene = first_scene
        project.save()

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        # Retorna apenas os projetos do usuário autenticado
        return Project.objects.filter(user=self.request.user)
    
class ProjectListViewPublic(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        """
        Retorna todos os projetos se o usuário for staff, 
        caso contrário, retorna apenas os projetos públicos.
        """
        user = self.request.user
        if user.is_staff:  # Verifica se o usuário tem cargo de staff
            return Project.objects.all()  # Retorna todos os projetos
        return Project.objects.filter(privacy=False)  # Retorna apenas os projetos públicos
    
class ProjectViewSetWithID(generics.ListAPIView): #Para endpoint
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get_queryset(self):
        # Obtém o ID do projeto a partir dos parâmetros da URL
        project_id = self.kwargs.get('pk')
        return Project.objects.filter(id=project_id)

class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerUpdate
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
        project = self.get_object()

        # Verifica se o projeto pertence ao usuário autenticado
        if project.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para modificar este projeto.")
        
        # Atualiza os campos enviados sem alterar os não enviados
        serializer.save()

        # Verifica se foi fornecido um novo ID de cena
        first_scene_id = self.request.data.get('first_scene')
        if first_scene_id:
            try:
                # Verifica se a cena existe
                first_scene = Scene.objects.get(id=first_scene_id)
                
                # Verifica se a cena já está associada a outro projeto
                if Project.objects.filter(first_scene=first_scene).exclude(id=project.id).exists():
                    raise ValidationError("Essa cena já está associada a outro projeto.")
                
                # Atualiza o campo first_scene
                project.first_scene = first_scene
                project.save()  # Salva a atualização do projeto
            except Scene.DoesNotExist:
                raise ValidationError("Cena não encontrada.")

class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('id')

        try:
            # Recupera o projeto pelo ID
            project = Project.objects.get(id=project_id)

            # Verifica se o usuário é o dono do projeto ou tem permissão de staff
            if project.user == request.user or request.user.is_staff:
                project.delete()  # Exclui o projeto
                return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna sucesso

            # Retorna 403 se o usuário não tiver permissão
            return Response({'detail': 'Você não tem permissão para deletar este projeto.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        except Project.DoesNotExist:
            # Retorna 404 se o projeto não for encontrado
            return Response({'detail': 'Projeto não encontrado.'}, 
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
    serializer_class = SceneSerializer

    def get_queryset(self):
        queryset = Scene.objects.all()
        scene_id = self.request.query_params.get('id')  # Obtém o parâmetro 'id' da query string
        
        if scene_id:
            queryset = queryset.filter(id=scene_id)  # Filtra apenas a cena com o ID fornecido

        return queryset

class SceneViewSetWithProjectID(generics.ListAPIView):
    serializer_class = SceneSerializer

    def get_queryset(self):
        # Pega o parâmetro 'project_id' da URL
        project_id = self.kwargs.get('pk')
        return Scene.objects.filter(project_id=project_id)

class SceneUpdateView(generics.UpdateAPIView):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()
    lookup_field = 'pk'  # Altera o campo de busca para 'pk'

    def patch(self, request, *args, **kwargs):
        scene_id = request.query_params.get('pk')  # Pega o 'pk' da query string
        if not scene_id:
            return Response({'error': 'ID não fornecido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scene = self.get_queryset().get(id=scene_id)
            # Atualize os campos com os dados recebidos no request.data
            for attr, value in request.data.items():
                setattr(scene, attr, value)
            scene.save()

            serializer = self.get_serializer(scene)
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
    
class ChoiceListViewWithProjectID(generics.ListAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        # Obtém o ID do projeto dos parâmetros da URL
        project_id = self.kwargs.get('project_id')
        
        if not project_id:
            raise NotFound("O ID do projeto é obrigatório.")

        # Filtra cenas relacionadas ao projeto
        scenes = Scene.objects.filter(project_id=project_id)

        # Filtra escolhas relacionadas às cenas filtradas
        queryset = Choice.objects.filter(from_scene__in=scenes)

        if not queryset.exists():
            raise NotFound("Nenhuma escolha encontrada para o projeto especificado.")

        return queryset

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
        
# Description

class DescriptionView(generics.RetrieveAPIView):
    """
    View para recuperar a descrição de um usuário específico.
    """
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Description.objects.none()
        return Description.objects.filter(user_id=user_id)

class DescriptionCreateView(generics.CreateAPIView):
    """
    View para criar uma nova descrição para um usuário.
    """
    serializer_class = DescriptionSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        if not user_id:
            raise ValidationError({'error': 'O campo user_id é obrigatório.'})
        serializer.save(user_id=user_id)

class DescriptionListView(generics.ListAPIView):
    """
    View para listar todas as descrições.
    """
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Description.objects.filter(user_id=user_id)
        return Description.objects.all()

class DescriptionUpdateView(generics.UpdateAPIView):
    """
    View para atualizar a descrição de um usuário específico.
    """
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Description.objects.none()
        return Description.objects.filter(user_id=user_id)

class DescriptionDeleteView(generics.DestroyAPIView):
    """
    View para excluir a descrição de um usuário específico.
    """
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Description.objects.none()
        return Description.objects.filter(user_id=user_id)
    
class GradeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

class GradeCreateView(generics.CreateAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()

    def perform_create(self, serializer):
        # Obtém o ID do projeto e do usuário do payload
        project_id = self.request.data.get('project')
        user_id = self.request.data.get('user')

        # Verifica se o projeto existe
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError("Projeto não encontrado.")

        # Verifica se o ID do usuário corresponde ao usuário autenticado
        if user_id != self.request.user.id:
            raise ValidationError("Você não pode avaliar em nome de outro usuário.")

        # Verifica se o usuário já avaliou o projeto
        if Grade.objects.filter(user=self.request.user, project=project).exists():
            raise ValidationError("Você já avaliou este projeto.")

        # Cria a avaliação associando o usuário autenticado e o projeto
        serializer.save(user=self.request.user, project=project)

class GradeListView(generics.ListAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

class GradeUpdateView(generics.UpdateAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

class GradeDeleteView(generics.DestroyAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar
      