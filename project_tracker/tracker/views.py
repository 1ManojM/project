from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from logs.models import TimeLog

@login_required
def dashboard(request):
    role = getattr(getattr(request.user, 'profile', None), 'role', None)
    projects = Project.objects.all()
    tasks = Task.objects.all()
    logs = TimeLog.objects.all()

    if role == 'PM':
        projects = projects.filter(manager=request.user)
        tasks = tasks.filter(project__manager=request.user)
        logs = logs.filter(task__project__manager=request.user)
    elif role == 'DEV':
        projects = projects.filter(tasks__assignee=request.user).distinct()
        tasks = tasks.filter(assignee=request.user)
        logs = logs.filter(user=request.user)

    kpis = {
        'projects': projects.count(),
        'tasks_open': tasks.exclude(status='DONE').count(),
        'tasks_done': tasks.filter(status='DONE').count(),
        'hours_total': float(sum([l.hours for l in logs])) if logs.exists() else 0.0,
    }
    return render(request, 'dashboard.html', {'kpis': kpis, 'projects': projects[:5], 'tasks': tasks[:5]})
