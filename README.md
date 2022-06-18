# Microservice for AMCEF internship application

## Guide:
Make sure you have Python, Django, fastAPI and requests modules installed \
\
First, you need to make migrations and apply them by running these commands 
(make sure you are in right directory)\
`python3 manage.py makemigrations Api`\
and then \
`python3 manage.py migrate`\
Finally you can start the microservice:\
`python3 manage.py runserver`\
\
The GUI of this microservice should be accessible at [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)\
and the API at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) and its respective sub-urls\
\
For more see documentation/manual 
