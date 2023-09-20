from django.urls import path
from . import views

# name ='home' is a kwarg

urlpatterns = [
    path('', views.home, name='home'),
    # PROJECTS
    path('projects/', views.ProjectList.as_view(), name='projects_index'),
    path('projects/<int:proj_id>/', views.projects_detail, name='projects_detail'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:pk>/update/',views.ProjectUpdate.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/',views.ProjectDelete.as_view(), name='projects_delete'),
    # TASKS
    path('projects/<int:proj_id>/add_task/', views.add_task, name='add_task'),
    path('projects/<int:proj_id>/tasks/<int:task_id>/', views.tasks_detail, name='tasks_detail'),
    path('tasks/<int:pk>/update/',views.TaskUpdate.as_view(), name='tasks_update'),
    path('tasks/<int:pk>/delete/',views.TaskDelete.as_view(), name='tasks_delete'),
    # COMMENTS
    path('projects/<int:proj_id>/tasks/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/delete/',views.CommentDelete.as_view(), name='comments_delete'),
    # REGISTRATION
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE
    path('profile/<int:prof_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profile/<int:prof_id>/add_photo/', views.add_photo, name='add_photo'),
    # TEAM
    path('team/', views.team, name='team'),


]
