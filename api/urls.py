from django.urls import path
from .views import ProjectView, ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView, ProjectViewSet, ProjectViewSetWithID
from .views import SceneView, SceneCreateView, SceneListView, SceneUpdateView, SceneDeleteView, SceneViewSet
from .views import ChoiceView, ChoiceCreateView, ChoiceListView, ChoiceUpdateView, ChoiceDeleteView, ChoiceViewSet
from .views import UserView, UserCreateView, UserListView, UserUpdateView, UserDeleteView

from rest_framework.routers import DefaultRouter

# adicionar os imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user', UserView.as_view(), name='user_list'),
    path('create/user', UserCreateView.as_view(), name='user_list'),
    path('list/user', UserListView.as_view(), name='user_list'),
    path('update/user', UserUpdateView.as_view(), name='user_list'),
    path('delete/user', UserDeleteView.as_view(), name='user_list'),

    path('project', ProjectView.as_view()),
    path('create/project', ProjectCreateView.as_view(), name='create_project'),
    path('list/project', ProjectListView.as_view(), name='project_list'),
    path('list/project/<int:pk>/',
        ProjectViewSetWithID.as_view({'get': 'retrieve'}), #Buscar Projeto por ID
        name='project_list_ID'),
    path('update/project', ProjectUpdateView.as_view(), name='project_update'),
    path('delete/project', ProjectDeleteView.as_view(), name='project_delete'),

    path('scene', SceneView.as_view()),
    path('create/scene', SceneCreateView.as_view(), name='scene_create'),
    path('list/scene', SceneListView.as_view(), name='scene_list'),
    path('update/scene', SceneUpdateView.as_view(), name='scene_update'),
    path('delete/scene', SceneDeleteView.as_view(), name='scene_delete'),

    path('choice', ChoiceView.as_view()),
    path('create/choice', ChoiceCreateView.as_view(), name='choice_create'),
    path('list/choice', ChoiceListView.as_view(), name='choice_list'),
    path('update/choice', ChoiceUpdateView.as_view(), name='choice_update'),
    path('delete/choice', ChoiceDeleteView.as_view(), name='choice_delete'),

    # obtenção do token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    # atualizar o token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


router = DefaultRouter()
router.register(r'project' , ProjectViewSet)
router.register(r'scene' , SceneViewSet)
router.register(r'choice' , ChoiceViewSet) 
