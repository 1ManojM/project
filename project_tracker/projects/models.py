from django.db import models
from django.contrib.auth.models import User
from clients.models import Client

STATUS_CHOICES = (
    ('PROSPECT','Prospect'),
    ('LEAD','Lead'),
    ('CONFIRMED','Confirmed'),
    ('IN_PROGRESS','In Progress'),
    ('ON_HOLD','On Hold'),
    ('REJECTED','Rejected'),
    ('DONE','Done'),
)

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROSPECT')

    class Meta:
        unique_together = ('client','name')

    def __str__(self):
        return self.name
