from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Profile, Task, Comment, User
from .forms import TaskForm, CommentForm
# registration imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# HOME


def home(request):
    return render(request, 'home.html')

# ABOUT


def about(request):
    return render(request, 'about.html')

# PROFILE


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profile/detail.html'


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['department']
    template_name = 'main_app/form.html'
    success_url = '/'

# REGISTRATION VIEWS


def team(request):
    tasks = Task.objects.filter()
    users = User.objects.filter()
    return render(request, 'team.html', {
        'tasks': tasks,
        'users': users,
    })

# TASK VIEWS


class TaskList(ListView):
    model = Task
    template_name = 'tasks/index.html'


def tasks_detail(request, proj_id, task_id):
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=proj_id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(task=task_id)
    return render(request, 'tasks/detail.html', {
        'project': project,
        'task': task,
        'comments': comments,
        'comment_form': comment_form
    })


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


class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'main_app/form.html'
    success_url = '/projects/'


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


# PROJECT VIEWS
class ProjectList(ListView):
    model = Project
    template_name = 'projects/index.html'


def projects_detail(request, proj_id):
    project = Project.objects.get(id=proj_id)
    tasks = Task.objects.filter(project=proj_id)
    task_form = TaskForm()
    return render(request, 'projects/detail.html', {
        # include the cat and feeding_form in the context
        'project': project,
        'tasks': tasks,
        'task_form': task_form
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('projects_index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
