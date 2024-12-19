from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm

# def students_list(request):
#     students = Student.objects.all()
#     return render(request, 'students/students_list.html', {'students': students})


def students_list(request):
    students = Student.objects.select_related('user').all()  # Use `select_related` for efficiency
    return render(request, 'students/students_list.html', {'students': students})

# def student_detail(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
    
#     return render(request, 'students/student_detail.html', {'student': student})


def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user'), id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})


# def student_add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the new student to the database
#             return redirect('students_list')  # Redirect to the student list after saving
#     else:
#         form = StudentForm()  # Display an empty form for GET requests
    
#     return render(request, 'students/students_add.html', {'form': form})

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Link with a User (modify this logic as per your requirements)
            user = User.objects.create_user(
                username=form.cleaned_data['passport'],  # Example: Use passport as username
                password='defaultpassword'  # Set a default password (should be updated later)
            )
            student.user = user
            student.save()
            return redirect('students_list')
    else:
        form = StudentForm()
    return render(request, 'students/students_add.html', {'form': form})


# def student_edit(request, pk):
#     student = get_object_or_404(Student, pk=pk)
    
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect('students_list')
#     else:
#         form = StudentForm(instance=student)
#     return render(request, 'students/students_form.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            # Update User details if needed
            user = student.user
            user.username = form.cleaned_data['passport']  # Example: Update username if necessary
            user.save()
            student.save()
            return redirect('students_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/students_form.html', {'form': form})

# def student_delete(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method == 'POST':
#         student.delete()
#         return redirect('students_list')
#     return render(request, 'students/students_confirm_delete.html', {'student': student})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        # Optionally delete the associated User
        student.user.delete()
        student.delete()
        return redirect('students_list')
    return render(request, 'students/students_confirm_delete.html', {'student': student})