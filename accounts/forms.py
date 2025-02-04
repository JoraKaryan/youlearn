from django import forms
from django.forms.widgets import DateInput
from .models import CustomUser
from students.models import Student

class CustomUserCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True)
    surname = forms.CharField(max_length=50, required=True)
    birthday = forms.DateField(
        required=False,
        widget=DateInput(attrs={'type': 'date'})
    )
    passport = forms.CharField(max_length=20, required=True)
    phone = forms.CharField(max_length=15, required=False, initial='')
    email = forms.EmailField(max_length=254, required=True)  # Email should be EmailField
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True)


    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'birthday', 'passport', 'phone', 'email', 'password'] # Explicit field order
        widgets = {'password': forms.PasswordInput()}

    def clean_passport(self):
        passport = self.cleaned_data.get('passport')
        # Check if a student with this passport already exists
        if Student.objects.filter(passport=passport).exists():
            raise forms.ValidationError("A student with this passport number already exists.")
        return passport

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
class CustomLoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)