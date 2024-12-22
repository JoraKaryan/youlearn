from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('students_list')  # Redirect based on role
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


User = get_user_model()  # Use the custom user model

def student_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Step 1: Use transaction to ensure both user and student are saved correctly
                with transaction.atomic():
                    # Step 2: Create and save the CustomUser first
                    user = User.objects.create_user(
                        email=form.cleaned_data['email'],
                        password='defaultpassword',  # Set a default password (should be updated later)
                        username=form.cleaned_data['email'],  # Assuming email is used as username
                    )
                    user.save()  # Ensure the user is saved before creating the student

                    # Step 3: Create the Student instance and associate it with the user
                    student = form.save(commit=False)  # Don't save the student yet
                    student.user = user  # Associate the created user with the student
                    student.save()  # Save the student

                return redirect('personal_page')  # Redirect to the students list or desired page
            except Exception as e:
                # Handle any exceptions that occur during the transaction
                print(f"Error: {e}")
                return render(request, 'registration/signup.html', {'form': form, 'error': str(e)})

    else:
        form = CustomUserCreationForm()

    return render(request, 'personal_page.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# @login_required
def personal_page(request):
    return render(request, 'personal_page.html')
