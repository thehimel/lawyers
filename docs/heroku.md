# Heroku Deployment Process
- [Instructions](https://devcenter.heroku.com/articles/deploying-python)
- [Deploying to Heroku Server by Dennis Ivy](https://youtu.be/kBwhtEIXGII)
- [Heroku Postgres Connection by Dennis Ivy](https://youtu.be/TFFtDLZnbSs)

## Important
Your heroku root is the directiory where manage.py stays. The heroku required files shoulw also stay on the same directory of manage.py.

Create a separate repo for heroku and copy all the cotenst of src on that repo and create the heroku required files.

##  Files required
- runtime.txt
- requirements.txt
- Procfile

## Step 1: Gunicorn
Used to run the python server on deployment. [Doc](https://docs.gunicorn.org/en/latest/settings.html)
> In '--log-file -', FILE_NAME is '-'. It enables the gunicorn log to stderr.

`pip install gunicorn`

Create 'Procfile' with:
web: gunicorn project_name.wsgi --log-file -

## Step 2: settings.production
```python
DEBUG = False
ALLOWED_HOSTS = ['www.your-website.com', 'ip-address',]
```

## Step 3: .gitignore
Make sure .env is included in the .gitignore so that this file does't go to the deployment repository.
Also make sure db.sqlite3 is included in the .gitignore.

## Step 4: Python Runtime
Check the Python version in your venv with `python --version` and add specify that in this file. It will let the Heroku server know which version of python to start with. Else, it will automatically select the latest available version.
Also check the heroku python runtime versions to match with your venv python version. After that decide the appropriate version.

[Link](https://devcenter.heroku.com/articles/python-support#specifying-a-python-version)

runtime.txt
python-3.7.9

## Step 5: Static Files

### STATIC_ROOT
Define STATIC_ROOT in the project settings. It will allow WhiteNoise to perform the collectstatic command and save all the static files in this directory.
```python
STATIC_ROOT = BASE_DIR / 'static'
```
> STATICFILES_DIRS is used to let Django know what the directories to look for your static files. You save your necessary static files i.e. css, js, img, etc. in the STATICFILES_DIRS and STATIC_ROOT is used for collectstatic.


### Serving static files from Django with WhiteNoise. [Doc](http://whitenoise.evans.io/en/stable/)

`pip install whitenoise`

Edit your settings.py file and add WhiteNoise to the MIDDLEWARE list, above all other middleware apart from Django’s SecurityMiddleware:

```python
MIDDLEWARE = [
  # 'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
]
```

## Step 6 Setup Postgres
Postgres DB is by default provided by Heroku and serves a DATABASE_URL in the env.
To fetch the DB configurations from this DATABASE_URL use dj-database-url. [Link](https://pypi.org/project/dj-database-url/)
Install and add the following lines in the settings.production file.

```bash
pip install dj-database-url
```

```python
import dj_database_url
DATABASE_URL = config('DATABASE_URL')
postgres_db = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
# DATABASES = {} is declared in the base.py
DATABASES['default'] = postgres_db
```

### Perform Postgres Migrations in the Heroku Server
- In you local machine turn DEBUG=False so that production postgres_bd is selected.
- Delete all the migration files and run the commands to perform the migrations on the postgres db.
- The migrate command will run bit slow which indicates that production db is selected.
```bash
python ./src/manage.py makemigrations
python ./src/manage.py migrate
```
- While pushing the files in the production repo, let the migrations files be present because heroku won't write anything in the repo. Thus, you need your migration files in the production repo.
- In summary, you can perform the makemigrations command in the local machine, then push it to the repo, and run the migrate command from the heroku command line in the heroku website. This is the easiest and fastest way.

## Step 7 Heroku [Link](https://www.heroku.com/)
- Login to your Heroku account.
- Create an app.
- Copy the app url and add it to the ALLOWED_HOSTS in project settings.
- Add addon Heroku Postgres
- Set the env variable for DEBUG, SECRET_KEY, EMAIL_USER, EMAIL_PASS
- Select Builpack as Python
- Select GitHub repo and deploy.

## Heroku Commands
```bash
heroku run python manage.py makemigrations --app mntest01
heroku run python manage.py migrate --app mntest01
```

## Add These Config Vars
DATABASE_URL (Automatically added after initializing Postgres addon)
DEBUG = False
EMAIL_PASS
EMAIL_USER
SECRET_KEY