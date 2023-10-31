
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('update_doctor/<int:doctor_id>/', views.update_doctor, name='update_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor')
]
