from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Student
from .forms import StudentForm

@login_required
def students_list(request):
    students = Student.objects.select_related('user').all()
    filters = {}  # Dictionary to store filter values

    # Filtering logic for each field
    name_query = request.GET.get('name')
    if name_query:
        students = students.filter(name__icontains=name_query)
        filters['name'] = name_query

    surname_query = request.GET.get('surname')
    if surname_query:
        students = students.filter(surname__icontains=surname_query)
        filters['surname'] = surname_query

    email_query = request.GET.get('email')
    if email_query:
        students = students.filter(user__email__icontains=email_query)
        filters['email'] = email_query

    group_query = request.GET.get('group')
    if group_query:
        students = students.filter(group__icontains=group_query)
        filters['group'] = group_query

    phone_query = request.GET.get('phone')
    if phone_query:
        students = students.filter(phone__icontains=phone_query)
        filters['phone'] = phone_query

    passport_query = request.GET.get('passport')
    if passport_query:
        students = students.filter(passport__icontains=passport_query)
        filters['passport'] = passport_query


    return render(request, 'students/students_list.html', {'students': students, 'filters': filters})

@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user'), id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})


User = get_user_model()  # Use the custom user model
@login_required
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
                        first_name=form.cleaned_data['name'],
                        last_name=form.cleaned_data['surname'],
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

@login_required
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

@login_required
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