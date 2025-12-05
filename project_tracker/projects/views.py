from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project
from .forms import ProjectForm

def is_admin(u): return hasattr(u, 'profile') and u.profile.role == 'ADMIN'
def is_pm(u): return hasattr(u, 'profile') and u.profile.role == 'PM'

@login_required
def project_list(request):
    role = getattr(request.user.profile, 'role', None)
    qs = Project.objects.select_related('client','manager')
    if role == 'PM':
        qs = qs.filter(manager=request.user)
    elif role == 'DEV':
        qs = qs.filter(tasks__assignee=request.user).distinct()
    return render(request, 'projects/list.html', {'projects': qs})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_pm(u))
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        proj = form.save()
        messages.success(request, 'Project created.')
        return redirect('projects:detail', pk=proj.pk)
    return render(request, 'projects/form.html', {'form': form})

@login_required
def project_detail(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    role = getattr(request.user.profile, 'role', None)
    if role == 'PM' and proj.manager != request.user:
        return redirect('projects:list')
    return render(request, 'projects/detail.html', {'project': proj})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_pm(u))
def project_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.user.profile.role == 'PM' and proj.manager != request.user:
        return redirect('projects:list')
    form = ProjectForm(request.POST or None, instance=proj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Project updated.')
        return redirect('projects:detail', pk=pk)
    return render(request, 'projects/form.html', {'form': form})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_pm(u))
def project_delete(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        proj.delete()
        messages.success(request, 'Project deleted.')
        return redirect('projects:list')
    return render(request, 'projects/confirm_delete.html', {'obj': proj})
