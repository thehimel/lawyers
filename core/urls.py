from django.urls import path
from core.views.common import HomeView, dashboard, AppointmentCreateView
from core.views.lawyers import (LawyerDashboardView,
                                LawyerProfileCreateView,
                                lawyer_profile_update,
                                LawyerProfileListView)
from core.views.customers import CustomerDashboardView


app_name = 'core'

urlpatterns = [
    # url: '/', name = core:home
    path('', HomeView.as_view(), name='home'),

    # url: '/lawyers/dashboard', name = core:lawyer_dashboard
    path('lawyers/dashboard',
         LawyerDashboardView.as_view(), name='lawyer_dashboard'),

    # url: '/customers/dashboard', name = core:customer_dashboard
    path('customers/dashboard',
         CustomerDashboardView.as_view(), name='customer_dashboard'),

    # url: '/dashboard', name = core:dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # url: '/lawyers/profile/create', name = core:lawyer_dashboard
    path('lawyers/profile/create',
         LawyerProfileCreateView.as_view(), name='lawyer_profile_create'),

    # url: '/lawyers/profile', name = core:lawyer_profile
    path('lawyers/profile', lawyer_profile_update, name='lawyer_profile'),

    # url: '/lawyers/', name = core:lawyers
    path('lawyers/',
         LawyerProfileListView.as_view(), name='lawyers'),

    # url: '/appointment/', name = core:appointment
    path('appointment/<int:pk>',
         AppointmentCreateView.as_view(), name='appointment'),
]
