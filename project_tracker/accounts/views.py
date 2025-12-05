from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, UserCreateForm

def is_admin(u):
    return hasattr(u, 'profile') and u.profile.role == 'ADMIN'

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User created.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form})
