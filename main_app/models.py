from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now

STATUS = (
    ('P', 'In Process'),
    ('H', 'On Hold'),
    ('C', 'Completed')
)

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    due_date = models.DateField(default=now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # one letter to represent the meal Breakfast Lunch Dinner
    status = models.CharField(
      max_length=1,
      #add choices field option that creates drop down
      choices=STATUS,
      default=STATUS[0][0]
    )
    # tasks = models.ForeignKey(Task, on_delete=models.CASCADE)