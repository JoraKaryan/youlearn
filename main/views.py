from django.shortcuts import render
from students.models import Student
from tutors.models import Tutor
from groups.models import Group

def homepage(request):
    students_count = Student.objects.count()
    tutors_count = Tutor.objects.count()
    groups_count = Group.objects.count()
    return render(request, 'main/homepage.html', {'students_count': students_count, 'tutors_count': tutors_count, 'groups_count': groups_count})

def no_permission(request):
    return render(request, 'main/no_permission.html', status=403)

