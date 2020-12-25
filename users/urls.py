from django.urls import path
from users.views.common import profile
from users.views.employees import EmployeeSignupView
from users.views.managers import ManagerSignupView

app_name = 'users'

urlpatterns = [
    # url: /users/profile | name: users:profile
    path('profile/', profile, name='profile'),

    # url: /users/employees/signup/ | name:  users:emp_signup
    path('employees/signup', EmployeeSignupView.as_view(), name='emp_signup'),

    # url: /users/managers/signup/ | name: users:man_signup
    path('managers/signup', ManagerSignupView.as_view(), name='man_signup'),
]
