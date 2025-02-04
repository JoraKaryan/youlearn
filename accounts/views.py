from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import CustomUser
from students.models import Student
from tutors.models import Tutor


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the user with a hashed password
                    user = CustomUser.objects.create_user(
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password'],
                        username=form.cleaned_data['email'],
                        # role=form.cleaned_data['role'],
                    )

                    # Common fields for both Student and Tutor
                    common_fields = {
                        'user': user,
                        'name': form.cleaned_data['name'],
                        'surname': form.cleaned_data['surname'],
                        'birthday': form.cleaned_data.get('birthday'),
                        'phone': form.cleaned_data.get('phone', '')
                    }

                    if user.role == 'student':
                        # Add passport only for students
                        common_fields['passport'] = form.cleaned_data['passport']
                        Student.objects.create(**common_fields)
                    # elif user.role == 'tutor':
                    #     Tutor.objects.create(**common_fields)

                    # Optionally log the user in
                    login(request, user)
                    return redirect('personal_page')

            except Exception as e:
                print(f"Error: {e}")
                # Log the error (avoid displaying detailed errors to the user)
                return render(request, 'accounts/registration/register.html', {
                    'form': form,
                    'error': 'An error occurred during registration. Please try again.'
                })

    else:
        print('------------GET--------------')
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your desired page after login
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def personal_page(request):
    return render(request, 'profile/personal_page.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('homepage')