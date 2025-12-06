from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('ADMIN', 'Admin'),
    ('PM', 'Project Manager'),
    ('DEV', 'Developer'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DEV')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
