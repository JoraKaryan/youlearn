from django.shortcuts import get_object_or_404, render, redirect
from .models import Student
from .forms import StudentForm

def students_list(request):
    students = Student.objects.all()
    return render(request, 'students/students_list.html', {'students': students})

def student_detail(request, student_id):
    # Fetch the student using the given student_id or return 404 if not found
    student = get_object_or_404(Student, id=student_id)
    
    return render(request, 'students/student_detail.html', {'student': student})

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new student to the database
            return redirect('students_list')  # Redirect to the student list after saving
    else:
        form = StudentForm()  # Display an empty form for GET requests
    
    return render(request, 'students/students_add.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/students_form.html', {'form': form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('students_list')
    return render(request, 'students/students_confirm_delete.html', {'student': student})
