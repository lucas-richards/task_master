from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project

# HOME
def home(request):
    return render(request, 'home.html')

# ABOUT
def about(request):
    return render(request, 'about.html')
  
# PROJECT VIEWS
class ProjectList(ListView):
  model = Project
  template_name = 'projects/index.html'

class ProjectDetail(DetailView):
  model = Project
  template_name = 'projects/detail.html'

# TASK VIEWS
# COMMENT VIEWS
# PROFILE VIEWS

