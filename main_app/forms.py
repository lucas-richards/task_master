from django.forms import ModelForm
from .models import Task, Comment

class TaskForm(ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description','owner', 'due_date']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content']