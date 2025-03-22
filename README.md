# **Customer service**

## About
This is a pet-project, it should not be used for commercial purposes!
<br/>This is a project for employees who can provide a service and customers who want to use it.

### Software that you need
* Python 3.11;
* Django 4.2;
* PostgreSQL.

### Technology stack:
* Python 3.11, Django 4.2;
* PostgreSQL;
* HTML & CSS.

### Getting Started

#### 1. Create database 'customer_service' in PostgreSQL.

#### 2. Create your '.env' file.
* Create '.env' file in the same directory as manage.py;
* Use the provided '.env.example' file as a reference to set the necessary environment variables.

#### 3. Install requirements and do migrations.
*  Install Poetry (if not already installed);
* `$ poetry install --with dev`;
* `$ python manage.py makemigrations`;
* `$ python manage.py migrate`.

#### 3.1. Set up pre-commit hooks
* `$ pre-commit install`;
* `$ pre-commit run --all-files`;
  * If you want to update pre-commit hooks to their latest versions, run: `$ pre-commit autoupdate`.


#### 4. Set up Google OAuth API
* Create Google OAuth API project on the Google Developers Console;
* Create a superuser for your Django project;
* Log in to the Django admin panel;
* Add your site by clicking on the "Sites";
  * Fill in the "Domain name" and the "Display name" field with http://127.0.0.1:8000;
* Add a social application by clicking on the "Social Applications".
  * Select "Google" as the provider and enter a name of your choice in the "Name" field;
  * Fill in the "Client id" and "Secret key" fields with the credentials from your Google OAuth API project;
  * Select the site that you created in form "Sites";
* Change the data in "Set up django-allauth" in settings.py, as needed.

#### 5. Set up Google Calendar API
* In the Google Cloud console, enable the Google Calendar API;
* Authorize credentials for a desktop application;
  * In the Google Cloud console, go to Menu > APIs & Services > Credentials;
  * Click Create Credentials > OAuth client ID;
  * Click Application type > Desktop app;
  * In the Name field, type a name for the credential. This name is only shown in the Google Cloud console;
  * Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret;
  * Click OK. The newly created credential appears under OAuth 2.0 Client IDs;
  * Save the downloaded JSON file as credentials.json, and move the file to your working directory;
  * Next add CLIENT_SECRET_JSON in .env file:
    * For instance: CLIENT_SECRET_JSON=credentials.json;
* Change the data in "Set up Google Calendar API" in settings.py, as needed.

Made by `Self`.
