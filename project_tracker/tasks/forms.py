from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('project','title','description','assignee','status','priority','estimate_hours','progress','due_date')
        widgets = {'due_date': forms.DateInput(attrs={'type':'date'})}
