from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('accounts/profile/', views.personal_page, name='personal_page'),
    path('register/', views.register, name='register'),
]