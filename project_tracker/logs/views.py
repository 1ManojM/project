from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TimeLog
from .forms import TimeLogForm

@login_required
def log_list(request):
    role = request.user.profile.role
    qs = TimeLog.objects.select_related('task','user','task__project')
    if role == 'PM':
        qs = qs.filter(task__project__manager=request.user)
    elif role == 'DEV':
        qs = qs.filter(user=request.user)
    return render(request, 'logs/list.html', {'logs': qs})

@login_required
def log_create(request):
    form = TimeLogForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        if request.user.profile.role == 'DEV':
            log.user = request.user
        else:
            log.user = request.user if not log.user_id else log.user
        log.save()
        messages.success(request, 'Time logged.')
        return redirect('logs:list')
    return render(request, 'logs/form.html', {'form': form})
