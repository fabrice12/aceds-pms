import json
# from lib2to3.fixes.fix_input import context
# from kafka import KafkaProducer

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from docutils.nodes import pending
from hdfs import InsecureClient
from kafka import KafkaProducer

from patients.forms import UserRegistrationForm, RendezvousForm
from patients.models import Rendezvous

# Kafka producer configuration
KAFKA_TOPIC = 'rendezvous_requests'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

HDFS_URL = "http://167.99.86.23:9870"
HDFS_PATH = "/appointments"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def home(request):
    return render(request, "index.html")


def register(request):
    form = UserRegistrationForm()
    context = {'form': form}
    return render(request, "register.html", context)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'PATIENT':
                return redirect('patient_dashboard')
            if user.user_type == 'ADMIN':
                return redirect('admin_dashboard')

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    return render(request, "login.html")


@login_required
def patient_dashboard(request):
    if request.user.user_type != 'PATIENT':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    form = RendezvousForm()

    rendezvous_requests = Rendezvous.objects.filter(patient=request.user).order_by('-request_date')
    ctx = {
        'form': form,
        'rendezvous_requests': rendezvous_requests,
    }
    return render(request, "patient_dashboard.html", ctx)


def create_rendezvous(request):
    if request.method == 'POST':
        form = RendezvousForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                # rendezvous = form.save(commit=False)
                # rendezvous.patient = request.user
                # rendezvous.save()
                client=InsecureClient(HDFS_URL,user='dr.who')
                file_path=None
                if 'file_path' in request.FILES:
                    file=request.FILES['file_path']
                    file_path=f'{HDFS_PATH}/{file.name}'
                    with client.write(f'{HDFS_PATH}/{file.name}', overwrite=True) as writer:
                        for chunk in file.chunks():
                            writer.write(chunk)
                # print file name





                rendezvous_data = {
                    'patient_id': request.user.id,  # Serialize patient ID
                    'department_id': form.cleaned_data['department'].id,  # Serialize department ID
                    'preferred_date': form.cleaned_data['preferred_date'].isoformat(),  # Serialize date
                    'urgency_level': form.cleaned_data['urgency_level'],
                    'symptoms': form.cleaned_data['symptoms'],
                    'contact_number': form.cleaned_data['contact_number'],
                    'insurance_provider': form.cleaned_data['insurance_provider'],
                    'additional_notes': form.cleaned_data['additional_notes'],
                    'file_path': file_path
                }

                # Send data to Kafka
                producer.send(KAFKA_TOPIC, rendezvous_data)
                producer.flush()  # Ensure the message is sen
                messages.success(request, "Rendezvous request created successfully.")

                if is_ajax(request):
                    return JsonResponse({"message": "Rendezvous request created successfully."})
                return redirect('patient_dashboard')



        except Exception as e:
            print(f"Error creating rendezvous: {e}")
            messages.error(request, "An error occurred while creating the rendezvous request.")
            return redirect('patient_dashboard')

    else:
        form=RendezvousForm()
    ctx={'form':form}
    if is_ajax(request):
        html=render_to_string('rendezvous_form.html',ctx,request=request)
        return JsonResponse({'html':html})
    return render(request,'rendezvous_form.html',ctx)

def rendezvous_update(request, pk):
    rendezvous = get_object_or_404(Rendezvous, pk=pk)
    if request.method == 'POST':
        form = RendezvousForm(request.POST, instance=rendezvous)
        if form.is_valid():
            form.save()
            if is_ajax(request):
                return JsonResponse({"message": "Author updated successfully"})
            return redirect('patient_dashboard')
    else:
        form = RendezvousForm(instance=rendezvous)
    ctx = {'form': form}
    if is_ajax(request):
        html = render_to_string('rendezvous_form.html', ctx, request=request)
        return JsonResponse({'html': html})
    return render(request, 'rendezvous_form.html', ctx)

def rendezvous_delete(request, pk):
    rendezvous = get_object_or_404(Rendezvous, pk=pk)
    if request.method == 'GET':
        rendezvous.delete()
        return redirect('patient_dashboard')

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'ADMIN':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')

        # SQL query to count patients above and below 18 using TIMESTAMPDIFF
    try:
        query = """
                    SELECT 
                        SUM(CASE WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) >= 18 THEN 1 ELSE 0 END) AS above_18,
                        SUM(CASE WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) < 18 THEN 1 ELSE 0 END) AS below_18
                    FROM patients_systemuser
                    WHERE user_type = 'PATIENT';
                """

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        # Extract counts
        above_18_count = result[0] or 0
        below_18_count = result[1] or 0

        total_pending_rdv=Rendezvous.objects.filter(status='PENDING').count()
        total_approved_rdv=Rendezvous.objects.filter(status='APPROVED').count()

        pending_rdvs=Rendezvous.objects.filter(status="PENDING").order_by('-request_date')[:10]

        for rdv in pending_rdvs:
            if rdv.file_path:
                rdv.download_file=f"{HDFS_URL}/webhdfs/v1{rdv.file_path}?op=OPEN"
        #         print file path
                print(rdv.download_file)



        # Pass the counts to the template
        context = {
            'above_18_count': above_18_count,
            'below_18_count': below_18_count,
            'total_pending_rdv':total_pending_rdv,
            'total_approved_rdv':total_approved_rdv,
            'pending_rdvs':pending_rdvs
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        messages.error(request, "An error occurred while fetching patient data.")
        context = {
            'above_18_count': 0,
            'below_18_count': 0,
        }

    return render(request, "admin_dashboard.html", context)


def register_create(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.user_type = 'PATIENT'
        user.password = make_password(form.cleaned_data['password'])
        user.username = form.cleaned_data['phone_number']
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('register')
    else:
        messages.error(request, "Registration failed. Please try again.")
        return render(request, "register.html", {'form': form})
