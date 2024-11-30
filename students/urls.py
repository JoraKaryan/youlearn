from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.students_list, name='students_list'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  # New URL for student detail

]
