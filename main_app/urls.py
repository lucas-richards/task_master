from django.urls import path
from . import views

# name ='home' is a kwarg

urlpatterns = [
    path('', views.ProjectList.as_view(), name='projects_index')

]