import json
from kafka import KafkaConsumer
from django.core.management.base import BaseCommand
from patients.models import Rendezvous, Department, SystemUser

KAFKA_TOPIC = 'rendezvous_requests'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

class Command(BaseCommand):
    help = 'Run the Kafka consumer to process rendezvous requests'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Kafka consumer...")

        # Initialize Kafka consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            group_id='rendezvous_group',
            auto_offset_reset='earliest'
        )

        # Consume messages from Kafka
        for message in consumer:
            self.stdout.write(f"Received message: {message.value}")
            self.save_to_database(message.value)

    def save_to_database(self, data):
        self.stdout.write("Saving rendezvous to database...")
        try:
            department = Department.objects.get(id=data['department_id'])
            patient = SystemUser.objects.get(id=data['patient_id'])

            # Save the rendezvous to the database
            Rendezvous.objects.create(
                patient=patient,
                department=department,
                preferred_date=data['preferred_date'],
                urgency_level=data['urgency_level'],
                symptoms=data['symptoms'],
                additional_notes=data['additional_notes'],
                contact_number=data['contact_number'],
                insurance_provider=data['insurance_provider'],
                file_path=data['file_path']

            )
            self.stdout.write(f"Rendezvous for patient {patient.id} saved successfully.")
        except Exception as e:
            self.stderr.write(f"Error saving rendezvous to database: {e}")