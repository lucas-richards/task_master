from django.forms import ModelForm
from .models import Task, Comment, User, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description','priority','status', 'assignee', 'due_date']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department']

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email']

