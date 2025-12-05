# from django.contrib import admin
# from django import forms
# from .models import Client

# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = '__all__'  # <-- This forces Django to use correct checkbox

# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     form = ClientForm
#     list_display = ('name', 'contact_person', 'email', 'phone', 'is_active')

from django.contrib import admin
from .models import Client
from .forms import ClientForm

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    list_display = ('name', 'contact_person', 'email', 'phone', 'is_active')
