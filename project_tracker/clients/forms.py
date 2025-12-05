# from django import forms
# from .models import Client

# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = ("name","contact_person","email","phone","notes","is_active")

from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "contact_person", "email", "phone", "notes", "is_active")
        widgets = {
            'is_active': forms.CheckboxInput(),   # <--- THE FIX
        }
