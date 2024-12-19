from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['name', 'surname', 'group', 'is_free', 'birthday', 'phone', 'id', 'passport', 'email']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        student = super().save(commit=False)
        email = self.cleaned_data.get('email')

        if email:
            if not student.user:
                user = User.objects.create_user(username=student.name, password='defaultpassword')
                student.user = user
            student.user.email = email
            if commit:
                student.user.save()
        if commit:
            student.save()
        return student