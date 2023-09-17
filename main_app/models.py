from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime, timedelta

STATUS = (
    ('P', 'In Process'),
    ('H', 'On Hold'),
    ('C', 'Completed')
)


# Comment


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)


class Project(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    three_months_future = datetime.now() + timedelta(days=90)
    due_date = models.DateField(default=three_months_future)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # one letter to represent the meal Breakfast Lunch Dinner
    status = models.CharField(
        max_length=1,
        # add choices field option that creates drop down
        choices=STATUS,
        default=STATUS[0][0]
    )
    # tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
