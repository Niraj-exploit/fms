from django import forms
from .models import Futsal
from userAuth.models import User
from django.forms.widgets import TextInput
from django.contrib.auth.hashers import make_password

class TimeInput(forms.TimeInput):
    input_type = "time"

class AddFutsalForm(forms.ModelForm):
    class Meta:
        model = Futsal
        fields = ['name', 'images', 'futsal_type', 'location', 'price', 'open_time', 'close_time', 'contact_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["open_time"].widget = TimeInput()
        self.fields["close_time"].widget = TimeInput()

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


# class UserCreationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
#     is_superuser = forms.BooleanField(label='Superuser', required=False)
#     is_active = forms.BooleanField(label='Active', required=False)
#     is_futsal_owner = forms.BooleanField(label='Futsal Owner', required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'name', 'bio', 'is_superuser', 'is_active', 'is_futsal_owner']
#         widgets = {
#             'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'height: 74px;'})
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if field_name not in ['is_superuser', 'is_active', 'is_futsal_owner']:
#                 field.widget.attrs.update({'class': 'form-control'})


# class UserCreationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
#     is_superuser = forms.BooleanField(label='Superuser', required=False)
#     is_active = forms.BooleanField(label='Active', required=False)
#     is_futsal_owner = forms.BooleanField(label='Futsal Owner', required=False)
#     image = forms.ImageField(label='Profile Image', required=False)  # Image field for the profile image

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'name', 'bio', 'is_superuser', 'is_active', 'is_futsal_owner', 'image']
#         widgets = {
#             'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'height: 74px;'}),
#             'image': forms.FileInput(attrs={'class': 'form-control-file'})  # Custom widget for the image field
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if field_name not in ['is_superuser', 'is_active', 'is_futsal_owner']:
#                 field.widget.attrs.update({'class': 'form-control'})


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    is_active = forms.BooleanField(label='Active', required=False)
    is_futsal_owner = forms.BooleanField(label='Futsal Owner', required=False)
    image = forms.ImageField(label='Profile Image', required=False)  # Image field for the profile image

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'bio', 'is_superuser', 'is_active', 'is_futsal_owner', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'style': 'height: 74px;'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})  # Custom widget for the image field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_superuser', 'is_active', 'is_futsal_owner']:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

