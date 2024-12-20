from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm

def students_list(request):
    students = Student.objects.select_related('user').all()  # Use `select_related` for efficiency
    return render(request, 'students/students_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user'), id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Link with a User (modify this logic as per your requirements)
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                password='defaultpassword',  # Set a default password (should be updated later)
                email=form.cleaned_data['email'], 
            )
            student.user = user
            student.save()
            return redirect('students_list')
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