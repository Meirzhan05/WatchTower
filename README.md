# WatchTower

## To run the frontend 
- navigate to ../frontend directory in your machine
- npm install
- npm install tailwindcss @tailwindcss/vite
- npm run dev

## To start frontend development
- download `ES7 React/Redux/GraphQL/React-Native snippets` in your VS code.
- create .js file and type `rcfe`.

## Backend intro video
- `https://www.youtube.com/watch?v=cJveiktaOSQ&t=486s&ab_channel=PedroTech`

## Backend Structure
```
/backend/               # Main project directory
├── backend/           # Project configuration directory
│   ├── asgi.py        
│   ├── settings.py    # in this file we declare the dependencies and env variables 
│   ├── urls.py        
│   ├── wsgi.py        
│   └── __init__.py
│
├── api/               # API application
│   ├── __init__.py
│   ├── serializers.py # Data serialization
│   ├── urls.py        # API route definitions
│   └── views.py       # API endpoint logic
│
├── cliquepay/         # Core Django app
│   ├── __init__.py
│   ├── admin.py      
│   ├── apps.py        
│   ├── aws_cognito.py # AWS Cognito integration
│   ├── db_service.py  # Database helper functions
│   ├── migrations/    # Database migrations
│   ├── models.py      # Database models
│   ├── tests.py       
│   └── views.py       
│
└── manage.py          # Django entry point
```

## Files that we mostly work on
- `backend/settings.py` : when we use new libraries or env variables
- `api/serializers.py` : Serializers convert incoming data from another language, typically JS for web/api stuff, into python objects.


- `api/urls.py` : to specify our backend api endpoints/urls.
- `api/views.py` : in this file we :
    1. set up the api functions, their content and logic (mostly request/response logic).
    2. set up views so that we as developers have a clean interface to view and test our api endpoints when the server is running.
- `cliquepay/aws_cognito.py` : user-authentication,etc. goes here
- `cliquepay/db_service.py` : all the functions that fetch or update anything to the database are here
- `cliquepay/models.py` : A Django model is the built-in feature that Django uses to create tables, their fields, and various constraints. Basically, we never directly execute queries in my sql, write the code in models and django takes care of it.

## To set up the development environment for Django
- install all the dependencies mentioned in the `requirements.txt` file using `pip install`.
- make sure you got all the environment variables using `.env.example` file.
- to set-up the database models execute:
    - `cd backend`
    - `python manage.py makemigrations`
    - `python manage.py migrate`
- You need to perform the above steps every time you change the database models.
- Execute `python manage.py runserver` to run your server on localhost.
- With that done, you're all set! 

## Common Errors/Mistakes
- If you encounter errors with your database, delete the `cliquepay/migrations` directory.
- run these again after addressing the errors:
    - `python manage.py makemigrations`
    - `python manage.py migrate`

## Working with git 
- always run `git fetch upstream`, followed by `git rebase upstream/main` before you start or end your work. (if you call the base (the main repository, not forked one) repository `upstream`)

## Django secret
- To generate a new Django secret key, you can use Django's built-in utility function. This can be done directly in a Python shell or within your Django project's `manage.py` shell

`>>from django.core.management.utils import get_random_secret_key`
`>print(get_random_secret_key())`
- This will output a new, randomly generated secret key that you can then copy and paste into your Django project's `settings.py` file as the value for `SECRET_KEY.Python`

`DJANGO_SECRET = 'your_new_secret_key'`
