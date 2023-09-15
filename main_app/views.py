from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project

# Create your views here.
  # TOYS VIEWS

class ProjectList(ListView):
  model = Project
  template_name = 'toys/index.html'



