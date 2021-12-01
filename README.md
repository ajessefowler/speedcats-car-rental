# Speedcats Car Rental
Full stack car rental website built for Columbus State Community College's capstone project. Allows customers to place and modify reservations, view inventories, and make payments online. A complete administrator site improves employee workflow, making common tasks such as updating inventories and running reports simple and easy.

## Screenshots
<img width="1348" alt="Screen Shot 2021-12-01 at 5 44 24 PM" src="https://user-images.githubusercontent.com/32973242/144326296-674004da-ece1-428d-8b19-5ea627bd79ea.png">

## Requirements

Python, Django, and a number of other dependencies are required by this project. If Python has been installed, the remaining dependencies, including Django, can be installed using the following command inside the speedcats-car-rental directory:

```
pip install -r requirements.txt
```

## Installing

Once all dependencies have been installed and the project has been cloned or downloaded, run the following commands to ensure the database is up to date:

```
python manage.py makemigrations
python manage.py migrate
```

Now, you should be able to start the server with the following command:

```
python manage.py runserver 
```
You will be able to access the site at http://127.0.0.1:8000, and the admin site at http://127.0.0.1:8000/admin. To create an account to login to the admin site, run the command:

```
python manage.py createsuperuser
```

and enter a name and password. You will now be able to login to the admin site, and you will be able to access the user-facing website.

## Built With

- Django
- Python
- PostgreSQL
- JavaScript
- HTML
- CSS
