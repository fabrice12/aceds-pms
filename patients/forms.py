from django import forms

from patients.models import SystemUser, Rendezvous


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'national_id', 'phone_number', 'email', 'password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'national_id': 'National ID',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',  # HTML5 native datepicker
                'class': 'form-control',  # Add Bootstrap styling
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder
                'autocomplete': 'off',  # Prevent browser autofill
            }),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class RendezvousForm(forms.ModelForm):
    class Meta:
        model = Rendezvous
        fields = ['department', 'preferred_date',  'symptoms', 'urgency_level',
                  'contact_number', 'additional_notes','insurance_provider','file_path']
        labels = {
            'department': 'Select Department',
            'preferred_date': 'Preferred Appointment Date',
            'preferred_time_slot': 'Preferred Time Slot',
            'symptoms': 'Describe Your Symptoms',
            'urgency_level': 'Urgency Level',
            'contact_number': 'Contact Number',
            'additional_notes': 'Additional Notes',
            'file_path': 'Upload File',
        }
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 native datepicker
                'class': 'form-control',  # Add Bootstrap styling
                'placeholder': 'YYYY-MM-DD',  # Optional placeholder
                'autocomplete': 'off',  # Prevent browser autofill
            }),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'file_path': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }
