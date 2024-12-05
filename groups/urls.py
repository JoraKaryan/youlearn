from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('groups/add/', views.group_add, name='group_add'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
]
