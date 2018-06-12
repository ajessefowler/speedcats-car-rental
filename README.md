# speedcats-car-rental
Summer 2018 CSCI Capstone Project

<h2>Installing</h2>

https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment

Follow these instructions to install Python, virtualenvwrapper, and Django (You will only install Django in your virutal environment. Name
your virtualenv 'speedcats' to follow along). Once you are in a virtualenv and have Django installed, cd to the speedcats directory in
Terminal or Command Prompt. The speedcats directory contains a file called 'manage.py'. Once there, run the commands...

'python manage.py makemigrations'
'python manage.py migrate'

Now, you should be able to start the server with the command 'python manage.py runserver'. You will be able to access the site at
http://127.0.0.1:8000, and the admin site at http://127.0.0.1:8000/admin. To create an account to login to the admin site, run the command
'python manage.py createsuperuser' and enter a name and password. Then, you can login and manipulate the data!

The following video from Harvard's CS50 is a great introduction to Django. After watching, you should be comfortable enough
to use Django for this project, and be able to appreciate its ease of use.

https://youtu.be/ZjAMRnCu-84
