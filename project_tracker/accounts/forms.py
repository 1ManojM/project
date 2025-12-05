from django import forms
from django.contrib.auth.models import User, Group

ROLE_CHOICES = (('ADMIN','Admin'),('PM','Project Manager'),('DEV','Developer'))

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # sync role & groups
            role = self.cleaned_data['role']
            profile = user.profile
            profile.role = role
            profile.save()
            user.groups.clear()
            group_map = {'ADMIN':'Admin','PM':'Project Manager','DEV':'Developer'}
            user.groups.add(Group.objects.get(name=group_map[role]))
        return user
