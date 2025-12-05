from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

TASK_STATUS = (('TODO','To Do'),('IN_PROGRESS','In Progress'),('REVIEW','In Review'),('DONE','Done'))
PRIORITY = (('LOW','Low'),('MEDIUM','Medium'),('HIGH','High'))

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='MEDIUM')
    estimate_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    progress = models.PositiveIntegerField(default=0)  # 0–100
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
