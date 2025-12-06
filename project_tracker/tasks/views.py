from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def is_admin_or_pm(u):
    return hasattr(u, 'profile') and u.profile.role in ('ADMIN','PM')

@login_required
def task_board(request):
    role = request.user.profile.role
    qs = Task.objects.select_related('project','assignee')
    if role == 'PM':
        qs = qs.filter(project__manager=request.user)
    elif role == 'DEV':
        qs = qs.filter(assignee=request.user)
    data = {
        'todo': qs.filter(status='TODO'),
        'inprogress': qs.filter(status='IN_PROGRESS'),
        'review': qs.filter(status='REVIEW'),
        'done': qs.filter(status='DONE'),
    }
    return render(request, 'tasks/board.html', data)

@login_required
@user_passes_test(is_admin_or_pm)
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        t = form.save()
        messages.success(request, 'Task created.')
        return redirect('tasks:detail', pk=t.pk)
    return render(request, 'tasks/form.html', {'form': form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    role = request.user.profile.role
    if role == 'PM' and task.project.manager != request.user:
        return redirect('tasks:board')
    if role == 'DEV' and task.assignee != request.user:
        return redirect('tasks:board')
    return render(request, 'tasks/detail.html', {'task': task})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    role = request.user.profile.role
    allowed = (role == 'ADMIN') or (role == 'PM' and task.project.manager == request.user) or (role == 'DEV' and task.assignee == request.user)
    if not allowed:
        return redirect('tasks:board')
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated.')
        return redirect('tasks:detail', pk=pk)
    return render(request, 'tasks/form.html', {'form': form})
