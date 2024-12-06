from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# def homepage(request):
#     return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('students.urls')),
    path('', include('courses.urls')),
    path('', include('groups.urls')),
    path('', include('tutors.urls')),
]
