from django.urls import path
from .views import ProjectView, ProjectCreateView, ProjectListView, ProjectUpdateView, ProjectDeleteView
from .views import SceneView, SceneCreateView, SceneListView, SceneUpdateView, SceneDeleteView
from .views import ChoiceView, ChoiceCreateView, ChoiceListView, ChoiceUpdateView, ChoiceDeleteView

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
]
