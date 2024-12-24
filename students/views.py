from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Student
from .forms import StudentForm

def students_list(request):
    students = Student.objects.select_related('user').all()  # Use `select_related` for efficiency
    return render(request, 'students/students_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user'), id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})

User = get_user_model()  # Use the custom user model

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                # Step 1: Use transaction to ensure both user and student are saved correctly
                with transaction.atomic():
                    # Step 2: Create and save the CustomUser first
                    user = User.objects.create_user(
                        email=form.cleaned_data['email'],
                        password='defaultpassword',  # Set a default password (should be updated later)
                        username=form.cleaned_data['email'],  # Assuming email is used as username
                        role='student'
                    )
                    user.save()  # Ensure the user is saved before creating the student

                    # Step 3: Create the Student instance and associate it with the user
                    student = form.save(commit=False)  # Don't save the student yet
                    student.user = user  # Associate the created user with the student
                    student.save()  # Save the student

                return redirect('students_list')  # Redirect to the students list or desired page
            except Exception as e:
                # Handle any exceptions that occur during the transaction
                print(f"Error: {e}")
                return render(request, 'students/students_add.html', {'form': form, 'error': str(e)})

    else:
        form = StudentForm()

    return render(request, 'students/students_add.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            # Update User details if needed
            user = student.user
            user.email = form.cleaned_data['email']  # Example: Update username if necessary
            user.username = user.email
            user.save()
            student.save()
            return redirect('students_list')
    else:
        initial_data = {'email': student.user.email if student.user else ''}
        form = StudentForm(instance=student, initial=initial_data)
    return render(request, 'students/students_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        # Optionally delete the associated User
        student.user.delete()
        student.delete()
        return redirect('students_list')
    return render(request, 'students/students_confirm_delete.html', {'student': student})

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('home')  # Prevent access if not a student
    return render(request, 'students/dashboard.html')