from django.urls import path
from . import views

# name ='home' is a kwarg

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # PROJECTS
    path('projects/', views.ProjectList.as_view(), name='projects_index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='projects_detail'),
    # TASKS
    # COMMENTS
    # REGISTRATION
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),


]