from django.urls import path
from . import views

urlpatterns = [
        path('', views.homepage, name='homepage'),
        path('no-permission/', views.no_permission, name='no_permission'),

]
