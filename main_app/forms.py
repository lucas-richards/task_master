from django.forms import ModelForm
from .models import Task, Comment, User, Profile
from django import forms

class TaskForm(ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description','assignee', 'due_date']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department']