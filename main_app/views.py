from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import TaskForm, CommentForm, UserUpdateForm, ProfileUpdateForm, RegistrationForm
from .models import Project, Profile, Task, Comment, User
from django.contrib.auth.decorators import login_required
# this is to restrict access to CBM or mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# registration imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# imports for photo
import uuid
import boto3
import os
import json

# HOME
def about(request):
    return render(request, 'about.html')

# PROFILE
class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profile/detail.html'

@login_required
def profile_detail(request, prof_id):
    profile = Profile.objects.get(id=prof_id)
    return render(request, 'profile/detail.html', {
        'profile': profile,
    })

@login_required
def profile_update(request, prof_id):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm( request.POST,
                                    request.FILES,
                                    instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request,f'Your account has been updated!')
            return redirect('profile_detail', prof_id=prof_id)
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm( instance= request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'prof_id':prof_id
    }
    return render(request, 'profile/form.html', context)
    

# REGISTRATION VIEWS


def my_tasks(request, user_id):
    tasks = Task.objects.filter(assignee = user_id)
    user = User.objects.get(id = request.user.id)
    return render(request, 'team.html', {
        'tasks': tasks,
        'user': user,
    })

# TASK VIEWS


class TaskList(ListView):
    model = Task
    template_name = 'tasks/index.html'

@login_required
def tasks_detail(request, proj_id, task_id):
    task = Task.objects.get(id=task_id)
    profile = Profile.objects.get(user=request.user)
    project = Project.objects.get(id=proj_id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(task=task_id)
    
    cannot_edit_task = not (profile.is_manager()
                            or task.is_assignee(request.user))
    user = request.user
    return render(request, 'tasks/detail.html', {
        'project': project,
        'profile': profile,
        'task': task,
        'comments': comments,
        'comment_form': comment_form,
        'cannot_edit_task': cannot_edit_task,
        'user': user

    })

@login_required
def add_task(request, proj_id):
    error_message = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.project = Project.objects.get(id=proj_id)
            new_task.created_by = request.user
            new_task.save()
            return redirect('projects_detail', proj_id=proj_id)
        else:
            error_message = 'Invalid sign up - try again'
    form = TaskForm()
    context = {'form': form, 'error_message': error_message,
               'class_name': 'Task'}
    return render(request, 'main_app/form.html', context)

@login_required
def edit_task(request, pk):
    error_message = ''
    task = Task.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    cannot_edit_task = not (
        profile.is_manager() or task.is_assignee(request.user))

    # when POST request, save information
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if cannot_edit_task:
            error_message = "Cannot update task"
        elif form.is_valid():
            edited_task = form.save(commit=False)
            edited_task.save()
            return redirect('tasks_detail', proj_id=task.project.id,task_id=task.id)
        else:
            error_message = 'Invalid task update'

    # if only GET, then just render form

    context = {
        'task': task,
        'form': TaskForm(instance=task),
        'profile': profile,
        'user': request.user,
        'cannot_edit_task': cannot_edit_task,
        'error_message': error_message
    }
    return render(request, 'tasks/edit.html', context)


class TaskDelete(DeleteView):
    model = Task
    template_name = 'main_app/confirm_delete.html'

    def get_success_url(self):
        task_pk = self.kwargs['pk']
        task_model = self.model
        task_query_array = task_model.objects.filter(id=task_pk)
        task = task_query_array[0]
        project_id = task.project.id  # type: ignore
        redirect_success_url = '/projects/' + str(project_id)
        return redirect_success_url


# # PROJECT VIEWS
# class ProjectList(ListView):
#     model = Project
#     template_name = 'projects/index.html'


def projects_index(request):
    projects = Project.objects.filter()
    profile = Profile.objects.get(user=request.user)
    return render(request, 'projects/index.html', {
        'projects': projects,
        "profile": profile
    })

@login_required
def projects_detail(request, proj_id):
    project = Project.objects.get(id=proj_id)
    tasks = Task.objects.filter(project=proj_id)
    task_form = TaskForm()
    profile = Profile.objects.get(user=request.user)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks,
        'task_form': task_form,
        "profile": profile
    })


class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'description', 'due_date']
    template_name = 'main_app/form.html'
    success_url = '/projects/'

    # This method creates a varible called class_name that is used in the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_name'] = 'Project'
        return context


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'due_date', 'status']
    template_name = 'main_app/form.html'
    success_url = '/projects/'


class ProjectDelete(DeleteView):
    model = Project
    template_name = 'main_app/confirm_delete.html'
    success_url = '/projects/'

# COMMENT VIEWS


def add_comment(request, proj_id, task_id):
    error_message = ''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.task = Task.objects.get(id=task_id)
            new_comment.user = request.user
            new_comment.project = Project.objects.get(id=proj_id)
            new_comment.save()
        else:
            error_message = 'Invalid sign up - try again'
    context = {'error_message': error_message}
    return redirect('tasks_detail', proj_id=proj_id, task_id=task_id)


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'main_app/confirm_delete.html'

    def get_success_url(self):
        comment_pk = self.kwargs['pk']
        comment_model = self.model
        comment_query_array = comment_model.objects.filter(id=comment_pk)
        comment = comment_query_array[0]
        project_id = comment.project.id  # type: ignore
        task_id = comment.task.id  # type: ignore
        redirect_success_url = '/projects/' + \
            str(project_id) + '/tasks/' + str(task_id)
        return redirect_success_url

# REGISTRATION VIEWS


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        print('this is the request.POST', request.POST)
        # form = UserCreationForm(request.POST)
        r_form = RegistrationForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)
        if r_form.is_valid() and p_form.is_valid():
            # This will add the user to the database
            user = r_form.save()
            profile = p_form.save(commit=False)  # Create a profile without saving it immediately
            profile.user = user  # Associate the profile with the user
            profile.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('projects_index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    r_form = RegistrationForm()
    p_form = ProfileUpdateForm()
    context = {
        'r_form': r_form, 
        'p_form': p_form, 
        'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# ADD PHOTO


def add_photo(request, prof_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    if photo_file:
        s3 = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to prof_id or prof (if you have a prof object)
            profile = Profile.objects.get(id=prof_id)
            profile.image_url = url
            profile.save()
            # Photo.objects.create(url=url, profile_id=prof_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('profile_detail', prof_id=prof_id)
