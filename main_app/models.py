from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date


STATUS = (
    ('P', 'In Process'),
    ('H', 'On Hold'),
    ('C', 'Completed')
)

PRIORITY = (
    ('H', 'High'),
    ('M', 'Medium'),
    ('L', 'Low')
)

DEPARTMENT = (
    ('Qua','Quality/Testing'),
    ('Dev','Developers'),
    ('Des','Design'),
    ('Arq','Arquitect'),
    ('Man','Manager'),
)

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(
      max_length=3,
      #add choices field option that creates drop down
      choices=DEPARTMENT,
      default=DEPARTMENT[0][0])
    image_url = models.CharField(default='/static/profile-image.jpeg',max_length=200)
    

class Project(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    three_months_future = datetime.now() + timedelta(days=90)
    due_date = models.DateField(default=three_months_future)
    # assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        # add choices field option that creates drop down
        choices=STATUS,
        default=STATUS[0][0]
    )

    def late(self):
        return self.due_date < date.today()
    
    
    
    class Meta:
        ordering = ['due_date']
    
    



class Task(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='owned_tasks', on_delete=models.CASCADE)
    three_months_future = datetime.now() + timedelta(days=90)
    due_date = models.DateField(default=three_months_future)
    created_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=STATUS[0][0]
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY,
        default=PRIORITY[0][0]
    )

    def late(self):
        return self.due_date < date.today()



# Comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

