from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from users.appvars import MANAGER, LAWYER, CUSTOMER


'''
Decorators to check the user type.
If the user doesn't pass the test, the user will redirect to '/'
which is achieved by defining login_url='/'.

Generally, a login url is used in the place of login_url.
But we are checking the login status with the login_required decorator
which handles the login of the user. If the user is not logged in,
the login_required decorator will redirect the user to log in.
'''


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


def lawyer_required(
        function=None,
        redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == LAWYER,
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator


def customer_required(
        function=None,
        redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == CUSTOMER,
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator


# user.address is not None means the user.address exists.
# If the address exists return True, else return False.
def test_address(user):
    try:
        user.address is not None
        return True
    except Exception:
        return False


# If the user fails the test redirect to the url mentioned in login_url
def user_has_address(function=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     login_url='users:address_create'):

    actual_decorator = user_passes_test(
        lambda u: test_address(u),
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator


# If lawyer profile exists, return False
def test_no_lawyer_profile(user):
    try:
        user.lawyerprofile is not None
        return False
    except Exception:
        return True


# If the user fails the test redirect to the url mentioned in login_url
def user_has_no_lawyer_profile(function=None,
                               redirect_field_name=REDIRECT_FIELD_NAME,
                               login_url='users:profile'):

    actual_decorator = user_passes_test(
        lambda u: test_no_lawyer_profile(u),
        redirect_field_name=redirect_field_name,
        login_url=login_url)

    if function:
        return actual_decorator(function)

    return actual_decorator
