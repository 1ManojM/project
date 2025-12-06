from django import forms
from .models import TimeLog

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ('task','date','hours','note')
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}
