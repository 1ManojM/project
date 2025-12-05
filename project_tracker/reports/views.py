from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from projects.models import Project

@login_required
def overview(request):
    return render(request, 'reports/overview.html')

@login_required
def project_data(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    statuses = ['TODO','IN_PROGRESS','REVIEW','DONE']
    labels = ['To Do','In Progress','In Review','Done']
    counts = [proj.tasks.filter(status=s).count() for s in statuses]
    return JsonResponse({'labels': labels, 'values': counts})
