from django.urls import path
from . import views

# name ='home' is a kwarg

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # PROJECTS
    path('projects/', views.ProjectList.as_view(), name='projects_index'),
    # path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='projects_detail'),
    path('projects/<int:proj_id>/', views.projects_detail, name='projects_detail'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:pk>/update/',views.ProjectUpdate.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/',views.ProjectDelete.as_view(), name='projects_delete'),
    # TASKS
    path('tasks/', views.TaskList.as_view(), name='tasks_index'),
    # path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='tasks_detail'),
    path('tasks/<int:task_id>/', views.tasks_detail, name='tasks_detail'),
    path('tasks/create/', views.TaskCreate.as_view(), name='tasks_create'),
    path('tasks/<int:pk>/update/',views.TaskUpdate.as_view(), name='tasks_update'),
    path('tasks/<int:pk>/delete/',views.TaskDelete.as_view(), name='tasks_delete'),
    # COMMENTS
    # REGISTRATION
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),


]
