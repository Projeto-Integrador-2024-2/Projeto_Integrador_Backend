from django.urls import path, include
from .views import CurrentUserView, GenreView, GenreCreateView, GenreListView, GenreUpdateView, GenreDeleteView
from .views import ProjectView, ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView, ProjectViewSet, ProjectViewSetWithID, ProjectListViewPublic
from .views import SceneView, SceneCreateView, SceneListView, SceneUpdateView, SceneDeleteView, SceneViewSet, SceneViewSetWithProjectID
from .views import ChoiceView, ChoiceCreateView, ChoiceListView, ChoiceUpdateView, ChoiceDeleteView, ChoiceViewSet, ChoiceListViewWithProjectID
from .views import DescriptionView, DescriptionCreateView, DescriptionListView, DescriptionUpdateView, DescriptionDeleteView
from .views import UserView, UserCreateView, UserListView, UserUpdateView, UserDeleteView
from .views import GradeCreateView, GradeDeleteView, GradeListView, GradeUpdateView, GradeView

from rest_framework.routers import DefaultRouter

# adicionar os imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user', UserView.as_view(), name='user_list'),
    path('create/user', UserCreateView.as_view(), name='user_list'),
    path('list/user', UserListView.as_view(), name='user_list'),
    path('update/user', UserUpdateView.as_view(), name='user_list'),
    path('delete/user', UserDeleteView.as_view(), name='user_list'),
    path('list/user/current', CurrentUserView.as_view(), name='user_current'),

    path('genre', GenreView.as_view()),
    path('create/genre', GenreCreateView.as_view(), name='genre_Create'),
    path('list/genre', GenreListView.as_view(), name='genre_list'),
    path('update/genre', GenreUpdateView.as_view(), name='genre_update'),
    path('delete/genre', GenreDeleteView.as_view(), name='genre_delete'),

    path('project', ProjectView.as_view()),
    path('create/project', ProjectCreateView.as_view(), name='create_project'),
    path('list/project', ProjectListView.as_view(), name='project_list'),
    path('list/project/public/', ProjectListViewPublic.as_view(), name='public-project-list'),  # Projetos públicos
    path('list/project/<int:pk>/', ProjectViewSetWithID.as_view(), name='project_list_ID'),
    path('update/project', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/project', ProjectDeleteView.as_view(), name='project_delete'),

    path('scene', SceneView.as_view()),
    path('create/scene', SceneCreateView.as_view(), name='scene_create'),
    path('list/scene', SceneListView.as_view(), name='scene_list'),
    path('list/scene/<int:pk>/', SceneViewSetWithProjectID.as_view(), name='scene_list_ID'),
    path('update/scene/<int:pk>/', SceneUpdateView.as_view(), name='scene_update'),
    path('delete/scene', SceneDeleteView.as_view(), name='scene_delete'),

    path('choice', ChoiceView.as_view()),
    path('create/choice', ChoiceCreateView.as_view(), name='choice_create'),
    path('list/choice', ChoiceListView.as_view(), name='choice_list'),
    path('list/choice/<int:project_id>/', ChoiceListViewWithProjectID.as_view(), name='choice_list_project'),
    path('update/choice', ChoiceUpdateView.as_view(), name='choice_update'),
    path('delete/choice', ChoiceDeleteView.as_view(), name='choice_delete'),

    path('description', DescriptionView.as_view()),
    path('create/description', DescriptionCreateView.as_view(), name='description_create'),
    path('list/description', DescriptionListView.as_view(), name='description_list'),
    path('update/description', DescriptionUpdateView.as_view(), name='description_update'),
    path('delete/description', DescriptionDeleteView.as_view(), name='description_delete'),

    # Rotas para Grade
    path('grade', GradeView.as_view(), name='grade_detail'),
    path('create/grade', GradeCreateView.as_view(), name='grade_create'),
    path('list/grade', GradeListView.as_view(), name='grade_list'),
    path('update/grade', GradeUpdateView.as_view(), name='grade_update'),
    path('delete/grade', GradeDeleteView.as_view(), name='grade_delete'),
    #GET /grade/ → Recupera um único objeto (com pk na requisição)
    #POST /create/grade/ → Cria um novo Grade
    #GET /list/grade/ → Lista todas as notas (Grade)
    #PUT /update/grade/ → Atualiza um Grade
    #DELETE /delete/grade/ → Remove um Grad
    
    # obtenção do token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    # atualizar o token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register(r'project' , ProjectViewSet)
router.register(r'scene' , SceneViewSet)
router.register(r'choice' , ChoiceViewSet) 
