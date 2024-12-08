from django.contrib import admin

from patients.models import Department, Rendezvous


# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','department_contact')  # Fields to display in the list view
    search_fields = ('name',)              # Fields to search by
    list_filter = ('name',)


@admin.register(Rendezvous)
class RendezvousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'department', 'doctor', 'request_date','assigned_date', 'preferred_date', 'urgency_level', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'department__name', 'doctor__first_name', 'doctor__last_name')
    list_filter = ('department', 'doctor', 'urgency_level', 'status')
    list_editable = ('status','doctor','assigned_date')


