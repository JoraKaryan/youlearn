from django.urls import path
from . import views

urlpatterns = [
    path('tutors/', views.tutors_list, name='tutors_list'),
    path('tutors/<int:pk>/edit/', views.tutor_edit, name='tutor_edit'),
    path('tutors/<int:pk>/delete/', views.tutor_delete, name='tutor_delete'),
    path('tutors/add/', views.tutor_add, name='tutor_add'),
    path('tutors/<int:tutor_id>/', views.tutor_detail, name='tutor_detail'),

]
