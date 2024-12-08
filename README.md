# Cloud Computing and Web Development Final Project
## Project Title: Hospital Appointments Management System
### Team Members:
-  DUSHIME Rene Fabrice 216073618: System Design & Architecture, Database Integration, Kafka Implementation, System Testing & Deployment

-  Mediatrice DUSENGE 218002150 : User interfaces Design, Frontend Development, Admin Dashboard Features, Documentation & Reporting

### Presentation video link: [Click here](https://drive.google.com/file/d/1BFESZC5GS4Lr7KnOMKysqHmfM4rYq372/view?usp=sharing)

https://drive.google.com/file/d/1BFESZC5GS4Lr7KnOMKysqHmfM4rYq372/view?usp=sharing

### Case Study:
In traditional healthcare environments, patients often face significant challenges when trying to see a doctor. A common scenario occurs when a patient visits a hospital, spends hours waiting, only to find out that the doctor is unavailable or not working that day. This results in wasted time, frustration, and dissatisfaction for the patient, as well as a negative perception of the hospital’s services. Such inefficiencies highlight a critical gap in hospital operations and patient communication, ultimately leading to poor service quality and resource mismanagement.
To address these issues, a **Hospital Appointments Management System (PMS)** was proposed and designed. This system enables patients to register and log in online, request appointments with specific doctors, and receive confirmation of availability before visiting the hospital

### Project Objectives:
The system's combination of strong management capabilities and user-friendly features is intended to empower healthcare facilities. Important goals consist of:

**Simplifying Appointment Requests:** By enabling patients to conveniently schedule doctor appointments online, manual scheduling and lengthy wait times are eliminated.

**Optimizing Administrative Control:** By accepting or rejecting appointment requests, administrators may effectively handle them and improve resource allocation.

**Giving Real-Time Insights:** The dashboard helps administrators keep an eye on system performance and make informed decisions by providing thorough statistics and analytics.

**Improving Communication and Efficiency:** The system facilitates smooth communication between patients and healthcare providers by centralizing information and automating repetitive procedures, which raises the standard of care overall.

For contemporary healthcare institutions, the Hospital Appointments Management System is an essential instrument that guarantees improved service delivery, operational effectiveness, and patient satisfaction


### Project Features:
The Hospital Appointments Management System is a comprehensive solution that includes a variety of features to meet the needs of both patients and administrators. The system's key features include:

**User Registration :** New users (patients) can access the Patients Management System using the registration interface with their Name, Phone_number, Email, Date of Birth,…. It should be made to capture important data while guaranteeing security, usability, and simplicity.

**User Login :** As the entry point for verified access, the login interface is an essential part of the patient management system. It guarantees that sensitive data and the system's functions are only accessible by authorized users, such as administrators, and patients.

**Patient Appointment Request :** The purpose of the Patient Appointment Request Interface is to facilitate the effective scheduling of medical appointments. By enabling patients to monitor doctor availability, choose convenient times, and make appointment requests and makedown their symptoms, this interface guarantees a flawless experience

**Analytics and Reporting :** The system's analytics and reporting capabilities provide administrators with real-time insights into system performance, patient activity, and resource utilization. By generating comprehensive reports and visualizations, administrators can make data-driven decisions and optimize system operations.

**Appointment Management :** The Appointment Management Interface is a critical feature that allows administrators to manage appointment requests effectively. By accepting or rejecting requests, administrators can ensure that appointments are scheduled efficiently and that resources are allocated appropriately.

### Project Architecture:
The Hospital Appointments Management System is built on a robust architecture that ensures scalability, reliability, and security. The system's architecture consists of 5 main components:

**Frontend Interface:** The frontend interface is the user-facing part of the system that enables patients to interact with the system. It includes the user registration, login, appointment request, and dashboard interfaces, which are designed to be intuitive, user-friendly, and responsive.

**Kafka Messaging System:** The Kafka messaging system is a distributed event streaming platform that enables real-time data processing and communication between system components. It is used to handle appointment requests and save it in topic and then send it to the database.

**Hadoop HDFS:** The Hadoop HDFS is a distributed file system that provides high-throughput access to application data. It is used to store patients' appointments file.

**AWS RDS MySQL Database:** The AWS RDS MySQL database is a managed relational database service that provides scalable, high-performance, and secure database storage. It is used to store patient data, appointment requests, and other system data.

### Project Technologies and libraries:
The Hospital Appointments Management System is built using a variety of technologies and libraries that enable its functionality and performance. The key technologies and libraries used in the system include:

**Frontend Technologies:** HTML, CSS, JavaScript, Bootstrap

**Backend Technologies:** Python Django, Kafka, Hadoop

**Database Technologies:** AWS RDS MySQL

**Libraries :** mysql-connector-python, kafka-python, hdfs

### Project Deployment:
To run this project on your local machine, you need to follow these steps:

**Step 1:** Clone the repository using the following command:

```git clone https://github.com/fabrice12/aceds-pms.git```

**Step 2:** Install the required libraries using the following command:

```pip install -r <library name>```

**Step 3:** Set database update the database settings in the settings.py file.

**Step 4:** Create a database using the following command:

```python manage.py migrate```

**Step 5:** Create a superuser using the following command:

```python manage.py createsuperuser```

**Step 7:** Set Kafka and HDFS configurations in the views.py file.:


**Step 9:** Run the Django server using the following command:

```python manage.py runserver```



