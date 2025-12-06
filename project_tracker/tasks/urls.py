from django.urls import path
from . import views
app_name = 'tasks'

urlpatterns = [
    path('', views.task_board, name='board'),
    path('create/', views.task_create, name='create'),
    path('<int:pk>/', views.task_detail, name='detail'),
    path('<int:pk>/edit/', views.task_edit, name='edit'),
]
