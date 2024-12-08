from django.contrib.auth.views import LogoutView
from django.urls import path
from sqlalchemy.dialects.mssql.information_schema import views

from patients.views import home, register, register_create, custom_login, patient_dashboard, admin_dashboard, \
    create_rendezvous, rendezvous_update

urlpatterns = [
    path('', home, name='home'),
    path('patient/register/', register, name='register'),
    path('patient/register/create', register_create, name='register_create'),
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('patient/create-rendezvous/', create_rendezvous, name='create_rendezvous'),
    path('patient/update-rendezvous/<int:pk>/', rendezvous_update, name='update_rendezvous'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
