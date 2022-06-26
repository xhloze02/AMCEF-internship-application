# Microservice for AMCEF internship application

## Guide:
Make sure you have Python, Django and requests modules installed \
Microservice uses SQLite3 database\
\
First, you need to make migrations and apply them by running these commands 
(make sure you are in a right directory)\
`python3 manage.py makemigrations api`\
and then \
`python3 manage.py migrate`\
Finally you can start the microservice:\
`python3 manage.py runserver`\
\
The GUI of this microservice should be accessible at [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)\
and the API at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) and its respective sub-urls\
\
For more see documentation/manual 
