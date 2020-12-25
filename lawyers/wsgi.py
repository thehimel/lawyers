"""
WSGI config for this project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/

In production, this is used file is used to run the app.
We are selected the SETTINGS_MODULE that is defined in the manage.py.
"""

import os
from django.core.wsgi import get_wsgi_application
from manage import SETTINGS_MODULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)
application = get_wsgi_application()
