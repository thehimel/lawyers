""" Global variables that can be used site-wide """

USERNAME_MAX_LENGTH = 30  # Used in project_directory/adpater.py

# Used in core.forms
# Used in users.models
FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MAX_LENGTH = 30

# Used in users.models
CATEGORY_MAX_LENGTH = 50

MANAGER = 'M'
LAWYER = 'L'
CUSTOMER = 'C'

USER_TYPE_CHOICES = [(MANAGER, 'Manager'),
                     (LAWYER, 'Lawyer'), (CUSTOMER, 'Customer')]

MAX_FILE_SIZE_IN_MB = 5
