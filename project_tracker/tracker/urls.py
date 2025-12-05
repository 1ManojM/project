from django.contrib import admin
from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('clients/', include('clients.urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('logs/', include('logs.urls')),
    path('reports/', include('reports.urls')),
    path('manoj/', dashboard, name='dashboard'),
]
