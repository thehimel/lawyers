from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from users.appvars import EMPLOYEE, MANAGER


'''
Decorators to check the user type.
If the user doesn't pass the test, the user will redirect to '/'
which is achieved by defining login_url='/'.

Generally, a login url is used in the place of login_url.
But we are checking the login status with the login_required decorator
which handles the login of the user. If the user is not logged in,
the login_required decorator will redirect the user to log in.
'''


def employee_required(
        function=None,
        redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == EMPLOYEE,
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator


def manager_required(
        function=None,
        redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == MANAGER,
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator
