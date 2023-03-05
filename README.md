# **Customer service**

## About
This is a pet-project, it should not be used for commercial purposes!
<br/>This is a project for employees who can provide a service and customers who want to use it.

### Software that you need
* Python 3.8.
* Django 3.2.
* PostgreSQL.

### Technology stack:
* Python 3.8, Django 3.2;
* PostgreSQL;
* HTML & CSS.

### Getting Started

#### 1. Create database 'customer_service' in PostgreSQL. 

#### 2. Create your '.env' file.
* Create '.env' file in the same directory as settings.py.
* Declare your environment variables in .env.
* File must contain: SECRET_KEY, DATABASE_NAME, DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET.    
* For example:
* `DATABASE_USER=postgres`

#### 3. Install requirements and do migrations.
* `$ pip install -r requirements.txt`.
* `$ python manage.py makemigrations`.
* `$ python manage.py migrate`.
* `$ python manage.py runserver`.

#### 4. Setup Google OAuth API

Made by `Self`.