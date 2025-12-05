from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client
from .forms import ClientForm

def is_admin_or_pm(u):
    return hasattr(u, 'profile') and u.profile.role in ('ADMIN','PM')

@login_required
def client_list(request):
    q = request.GET.get('q','')
    qs = Client.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, 'clients/list.html', {'clients': qs, 'q': q})

@login_required
@user_passes_test(is_admin_or_pm)
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Client created.')
        return redirect('clients:list')
    return render(request, 'clients/form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_pm)
def client_edit(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Client updated.')
        return redirect('clients:list')
    return render(request, 'clients/form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_pm)
def client_delete(request, pk):
    obj = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Client deleted.')
        return redirect('clients:list')
    return render(request, 'clients/confirm_delete.html', {'obj': obj})
