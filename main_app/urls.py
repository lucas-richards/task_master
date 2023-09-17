from django.urls import path
from . import views

# name ='home' is a kwarg

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # PROJECTS
    path('projects/', views.ProjectList.as_view(), name='projects_index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='detail'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:pk>/update/',
         views.ProjectUpdate.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/',
         views.ProjectDelete.as_view(), name='projects_delete'),
    # TASKS
    path('tasks/', views.task_list, name='task_list'),
    # COMMENTS
    # REGISTRATION
    path('accounts/signup/', views.signup, name='signup'),

]
