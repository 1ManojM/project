from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task

class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} - {self.task} - {self.hours}h"
