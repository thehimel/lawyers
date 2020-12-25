#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


PROJECT_NAME = 'djpro'

# For Development use 'settings/development.py'
# For Production use 'settings/production.py'
DEBUG = config('DEBUG', cast=bool)

if DEBUG:
    SETTINGS_MODULE = f'{PROJECT_NAME}.settings.development'
else:
    SETTINGS_MODULE = f'{PROJECT_NAME}.settings.production'


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
