from django.urls import path
from .views import ProjectCreateView, ProjectListView, SceneView, ChoiceView

urlpatterns = [
    path('project/create', ProjectCreateView.as_view()),
    path('project/list', ProjectListView.as_view()),
    path('scene', SceneView.as_view()),
    path('choice', ChoiceView.as_view()),
]
