from django.urls import path
from .views import ProjectView, ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView, ProjectViewSet
from .views import SceneView, SceneCreateView, SceneListView, SceneUpdateView, SceneDeleteView, SceneViewSet
from .views import ChoiceView, ChoiceCreateView, ChoiceListView, ChoiceUpdateView, ChoiceDeleteView, ChoiceViewSet
from .views import UserListView, UserCreateView

from rest_framework.routers import DefaultRouter

# adicionar os imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('project', ProjectView.as_view()),
    path('create/project', ProjectCreateView.as_view()),
    path('list/project', ProjectListView.as_view()),
    path('update/project', ProjectUpdateView.as_view()),
    path('delete/project', ProjectDeleteView.as_view()),

    path('scene', SceneView.as_view()),
    path('create/scene', SceneCreateView.as_view()),
    path('list/scene', SceneListView.as_view()),
    path('update/scene', SceneUpdateView.as_view()),
    path('delete/scene', SceneDeleteView.as_view()),

    path('choice', ChoiceView.as_view()),
    path('create/choice', ChoiceCreateView.as_view()),
    path('list/choice', ChoiceListView.as_view()),
    path('update/choice', ChoiceUpdateView.as_view()),
    path('delete/choice', ChoiceDeleteView.as_view()),

    path('list/user', UserListView.as_view(), name='user_list'),
    path('create/user', UserCreateView.as_view(), name='user_list'),


    # obtenção do token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    # atualizar o token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


router = DefaultRouter()
router.register(r'project' , ProjectViewSet)
router.register(r'scene' , SceneViewSet)
router.register(r'choice' , ChoiceViewSet) 
