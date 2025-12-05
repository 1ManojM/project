from django.urls import path
from . import views
app_name = 'reports'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('project/<int:pk>/data/', views.project_data, name='project_data'),
]
