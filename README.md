# lawyers
A Django project that illustrates the implementation of apppointment booking for lawyers.

## Deployment

[https://thelawyers.herokuapp.com/](https://thelawyers.herokuapp.com/)

## Important Package Versions
- python==3.7
- Django==3.1
- django-allauth==0.42.0
- django-crispy-forms==1.9.2
- django-cleanup==5.0.0
- django-multiselectfield==0.1.12
- django-countries==7.0
- mdb==4.19.1
- bootstrap==4
- django-bootstrap-datepicker-plus==3.0.5
- cloudinary==1.24.0
- django-cloudinary-storage==0.3.0
- django-money==1.2.2

## Other Important Packages
- psycopg2 - for managing postgres db
- dj-database-url - for postgres db url
- gunicorn - for running python server in heroku
- whitenoise - to server static files by running collecstatic in heroku
- django-cleanup - to delete files when user updates a filefield
- django-multiselectfield - to allow users select multiple choices
- django-countries - to show countries as dropdown list
- django-bootstrap-datepicker-plus - used for datepicker and timepicker
- cloudinary and django-cloudinary-storage - to store media files
- django-money - for currency management

## Getting Started
Create and activate virtual env with Miniconda and install dependencies.
```bash
conda create --name law python=3.7
conda activate mut
pip install -r requirements.txt
```

## Running the Server
Navigate inside directory src.
```bash
python manage.py runserver
```

## Changing Project Name
[Script]('./src/core/management/commands/rename.py')

Command
```bash
# Syntax: python manage.py rename <present_project_name> <new_project_name>
python manage.py rename current_project my_project
```

## Generating SECRET_KEY

### Method 1
```bash
python manage.py shell
```
```python
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```

### Method 2
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## User Types
A company having 3 types of users: Lawyer, Customer, and Manager.

allauth has default SignupForm, SignupView. Do not override it. Let it be remain at accounts/signup. And do not change the signup form in the settings.py for allauth - it will override the save method and won't allow our employee and manager signup views to save anything extra.

We have customized the following files for the tasks below.
users/forms/, users/views/, templates/users

1. Lawyer
Create custom signup form for lawyer.
Create custom signup view for lawyer.
You must use a custom template in this signup view.

2. Customer
Create custom signup form for customer.
Create custom signup view for customer.
You must use a custom template in this signup view.

3. Managers are created internally from admin panel.

## Permissions
- Appointment Acceptance
    - Only the lawyer can accept the appointment
- Appointment Cancellation
    - Customer, Lawyer, or Manager can cancel an appointment at any time.

## Frontend
Boostrap 4.5.3 is used for frontend. [Link](https://getbootstrap.com/docs/4.5/getting-started/introduction/)

Design of base.html
It was designed with the index.html file from mbd4 and allauth base.html.

Integrate Bootstrap with all the html files inside templates/account.
The account folder is downloaded from the template directory of allauth github repository.

## Deletion of Files Changed by the User
You use django-cleanup to remove files when user updates a filefiled. [Link](https://pypi.org/project/django-cleanup/)
Files used in defaults won't get deleted.

You can also use django-unused-media when you already have junk files. [Link](https://pypi.org/project/django-unused-media/)
This is a command line tool that can delete unused files.

## Important Notes
### email_confirmation_subject
In the database, you must rename the site to include your site_name in emails.
You must change the default email_confirmation_subject. Changing a little bit will be enough. Otherwise it will add [example.com] in the subject.

'src/templates/account/email/email_confirmation_subject.txt'
Default: Please Confirm Your E-mail Address
Customized: Please Confirm The E-mail Address

### Solution to Heroku Internal Server Error 500 on Sending Email using Gmail SMTP
- [Allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en)
- [Display Unlock Captcha](https://accounts.google.com/DisplayUnlockCaptcha)
- Display Unlock Captcha is very very important, else it will block login from heroku app.

### Best Solution to Heroku Internal Server Error 500 on Sending Email using Gmail SMTP
- Activate 2 Factor Authentication in your Google account.
- Create an app password for mail. You'll get a 15 digit code. Add it in the place of password in the env.
- Option for creating app password is available after the activation of 2 Factor Authentication.

### Internal Server Error 500
- Make sure you have added the domain in the ALLOWED_HOSTS of settings/production.py
- If you want to see the DEBUG information while in production, set PRO_DEBUG = True in env.
- The resize_image() function can cause Internal Server Error 500. Just comment that line, run the server once, create a user, and then you can uncomment it. It won't cause problem anymore. The exact reason of this bug is unknown.
- If appointment booking confirmation email or another email is not being sent, allow Display Unlock Captcha once again.
- Make sure you have kept the user_pro_pic inside the media/APP_NAME/defaults/img/user_pro_pic.jpg in the Cloudinary.

### Collectstatic
If you run 'python manage.py collectstatic', it will collect the static files of all associated apps and save it in a directory named 'static'.
You can delete this directory anytime. Our static files are save in directory named 'static_files'.

### Solution to Cloud Migration Not Taking Place from Local Machine
- Reason: Project is not Taking Environment Variable from System.
- Solution: Terminal needs to be restarted after updating the environment variables in Windows. If you are using vscode, open a new terminal or restart the vscode to take the updated environment variables from the system.

## Production Status
Is the project production ready?
Yes

## References
- [GFG](https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/)
- [pyblog](https://github.com/thehimel/pyblog)
- [django-boilerplate](https://github.com/thehimel/django-boilerplate)
- [django-multi-user-types](https://github.com/thehimel/django-multi-user-types)
- [django-multi-user-types-bs](https://github.com/thehimel/django-multi-user-types-bs)
