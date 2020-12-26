from django.urls import path
from users.views.common import profile, AddressCreateView
from users.views.lawyers import LawyerSignupView
from users.views.customers import CustomerSignupView


app_name = 'users'

urlpatterns = [
    # url: /users/profile | name: users:profile
    path('profile/', profile, name='profile'),
    path('address/new/', AddressCreateView.as_view(), name='address_create'),

    # url: /users/lawyers/signup/ | name: users:lawyer_signup
    path('lawyers/signup', LawyerSignupView.as_view(), name='lawyer_signup'),

    # url: /users/customers/signup/ | name:  users:customer_signup
    path('customers/signup',
         CustomerSignupView.as_view(), name='customer_signup'),
]
