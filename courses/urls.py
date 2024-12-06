from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
]
