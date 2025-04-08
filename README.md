# IITJ Health Care [![Deployed](https://img.shields.io/badge/Hosted_on-Azure-blue?logo=windows)](http://iitjhealthcaresk17.azurewebsites.net/) ![Status finished](https://img.shields.io/badge/Status-finished-2eb3c1.svg) ![Django 5.2](https://img.shields.io/badge/Django-5.2-green.svg) ![Python 3.10.2](https://img.shields.io/badge/Python-3.10.2-blue.svg) ![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)
----------------------------
ABOUT THE PROJECT
----------------------------
This project provides students online access to Health Centre and Medical Store.
The students can get online prescriptions from doctors, request ambulance in
emergency situations and get information about the medicines available in the
Medical Store.

🚀 **Hosted at:** [http://iitjhealthcaresk17.azurewebsites.net/](http://iitjhealthcaresk17.azurewebsites.net/)

----------------------------
SOFTWARE ENGINEERING PARADIGMS
----------------------------

The various aspects of software engineering applied to this project can be found
in 'ProjectPresentation.pdf'.

----------------------------
TECHNOLOGIES USED
----------------------------

- Python 3.10.2
- Django 5.2
- SQLLite
- Bootstrap ( HTML / CSS / Javascript )

----------------------------
INSTRUCTIONS TO RUN THE PROJECT
----------------------------

Type the following commands in sequential order:

              python3 -m venv venv      (To create virtual environment)
              pip install -r requirements.txt
              cd IITJHealthCare
              python3 manage.py migrate
              python3 manage.py runserver  

To deactivate the virtual environment:

              deactivate               

Following are the users for the project:

Patients(Can be registered through website register route):

- email : sk@iitj.ac.in         password : shashwat
- email : mm@iitj.ac.in         password : mayank
- email : mk@iitj.ac.in         password : manish
- email : sm@iitj.ac.in         password : shreyas

Doctors(Can be registered only through superuser):

- email : rpgoyal@iitj.ac.in    password : rpgoyal@iitj.ac.in
- email : nksingh@iitj.ac.in    password : nksingh@iitj.ac.in
- email : kumar.5@iitj.ac.in    password : kumar.5@iitj.ac.in
- email : sharma.1@iitj.ac.in   password : sharma.1@iitj.ac.in

----------------------------
# Health Centre
----------------------------

This folder contains the Health Centre application of the django project which includes online prescriptions, patients and doctors and other related
information. Main logic and code lies inside static folder, templates folder,
views.py, models.py ,tests.py and urls.py.

----------------------------
# Medical Store
----------------------------

This folder contains the Medical Store application which include the details
regarding medicines available in the medical store. Main logic and code lies
inside static folder, templates folder, views.py, models.py ,tests.py and
urls.py.

----------------------------

