import os
from django.core.management.base import BaseCommand


"""
Command to rename the Django project.
Usage: python manage.py rename <current_project_name> <new_project_name>
Example: python manage.py current_project my_project
"""


class Command(BaseCommand):
    help = 'Renames a Django project'

    def add_arguments(self, parser):
        parser.add_argument('current', type=str, nargs='+',
                            help='The current Django project folder name')
        parser.add_argument('new', type=str, nargs='+',
                            help='The new Django project name')

    def handle(self, *args, **kwargs):
        current_project_name = kwargs['current'][0]
        new_project_name = kwargs['new'][0]

        # logic for renaming the files

        # List of files to rename
        files_to_rename = ['manage.py', ]

        # files_to_rename = ['manage.py',
        #                    f'{current_project_name}/settings/base.py', ]

        for f in files_to_rename:
            # Read the file and store the contents in a variable
            with open(f, 'r') as file:
                filedata = file.read()

            # Replace all occurrences of that word in the variable
            filedata = filedata.replace(current_project_name, new_project_name)

            # Write all contents inside that variable in the file
            with open(f, 'w') as file:
                file.write(filedata)

        # Rename the directory
        os.rename(current_project_name, new_project_name)

        # Print the success message
        self.stdout.write(self.style.SUCCESS(
            'Project has been renamed to %s' % new_project_name))
