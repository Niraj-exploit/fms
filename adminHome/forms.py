from django import forms
from .models import Futsal
from userAuth.models import User
from django.forms.widgets import TextInput

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


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    is_active = forms.BooleanField(label='Active', required=False)
    is_futsal_owner = forms.BooleanField(label='Futsal Owner', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'bio', 'is_superuser', 'is_active', 'is_futsal_owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_superuser', 'is_active', 'is_futsal_owner']:
                field.widget.attrs.update({'class': 'form-control'})