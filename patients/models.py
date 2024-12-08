from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
HDFS_URL = "http://167.99.86.23:9870"
class SystemUser(AbstractUser):
    USER_TYPES=(
        ('ADMIN','Admin'),
        ('DOCTOR','Doctor'),
        ('PATIENT','Patient'),
    )
    user_type=models.CharField(max_length=20,choices=USER_TYPES,default='ADMIN')
    national_id=models.CharField(max_length=20,unique=True)
    phone_number=models.CharField(max_length=20,unique=True)
    date_of_birth=models.DateField(null=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    department_contact = models.CharField(max_length=100, null=True, blank=True)
    doctors = models.ManyToManyField(SystemUser, related_name='doctors', blank=True,limit_choices_to={'user_type':'DOCTOR'})

    def __str__(self):
        return self.name

class Rendezvous(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]



    URGENCY_CHOICES = [
        ('ROUTINE', 'Routine'),
        ('URGENT', 'Urgent'),
        ('EMERGENCY', 'Emergency'),
    ]

    patient = models.ForeignKey(
        SystemUser,
        on_delete=models.CASCADE,
        related_name='rendezvous_requests',
        limit_choices_to={'user_type': 'PATIENT'}
    )
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='rendezvous_requests')
    doctor = models.ForeignKey(
        SystemUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_rendezvous',
        limit_choices_to={'user_type': 'DOCTOR'}
    )
    request_date = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='ROUTINE')
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    assigned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reply = models.TextField(null=True, blank=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)

    def get_download_url(self):
        return f"{HDFS_URL}/webhdfs/v1{self.file_path}?op=OPEN"