
from django import forms
from django.contrib.auth.models import User
from .models import Tutor

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['name', 'surname', 'experience', 'information']

    def save(self, commit=True):
        tutor = super().save(commit=False)
        email = self.cleaned_data.get('email')

        if email:
            if not tutor.user:
                user = User.objects.create_user(username=tutor.name, password='defaultpassword')
                tutor.user = user
            tutor.user.email = email
            if commit:
                tutor.user.save()
        if commit:
            tutor.save()
        return tutor