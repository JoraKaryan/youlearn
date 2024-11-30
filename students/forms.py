
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'group', 'is_free', 'birthday', 'phone', 'id', 'passport']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }