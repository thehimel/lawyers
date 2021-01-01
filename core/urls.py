from django.urls import path
from core.views.common import (HomeView, dashboard,
                               AppointmentCreateView, AppointmentListView,
                               AppointmentCancelView)
from core.views.lawyers import (LawyerDashboardView, LawyerProfileCreateView,
                                LawyerProfileListView, LawyerProfileDetailView,
                                lawyer_profile_update, AppointmentAcceptView)
from core.views.customers import CustomerDashboardView
from core.views.managers import ManagerDashboardView, VerifyLawyerProfileView


app_name = 'core'

urlpatterns = [
    # url: '/', name = core:home
    path('', HomeView.as_view(), name='home'),

    # url: '/managers/dashboard', name = core:manager_dashboard
    path('managers/dashboard/',
         ManagerDashboardView.as_view(), name='manager_dashboard'),

    # url: '/lawyers/dashboard/', name = core:lawyer_dashboard
    path('lawyers/dashboard/',
         LawyerDashboardView.as_view(), name='lawyer_dashboard'),

    # url: '/customers/dashboard', name = core:customer_dashboard
    path('customers/dashboard/',
         CustomerDashboardView.as_view(), name='customer_dashboard'),

    # url: '/dashboard', name = core:dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # url: '/lawyers/profile/create', name = core:lawyer_dashboard
    path('lawyers/profile/create/',
         LawyerProfileCreateView.as_view(), name='lawyer_profile_create'),

    # url: '/lawyers/profile', name = core:lawyer_profile
    path('lawyers/profile/', lawyer_profile_update, name='lawyer_profile'),

    # url: '/lawyers/', name = core:lawyers
    path('lawyers/',
         LawyerProfileListView.as_view(), name='lawyers'),

    # url: '/lawyers/1', name = core:lawyer
    path('lawyers/<int:pk>/',
         LawyerProfileDetailView.as_view(), name='lawyer'),

    # url: '/lawyers/verify/1', name = core:verify
    path('lawyers/verify/<int:pk>/',
         VerifyLawyerProfileView.as_view(), name='verify'),

    # url: '/appointments/1', name = core:appointment
    path('appointments/<int:pk>/',
         AppointmentCreateView.as_view(), name='appointment_create'),

    # url: '/appointments/', name = core:appointments
    path('appointments/', AppointmentListView.as_view(), name='appointments'),

    # url: '/appointments/accept/', name = core:appointment
    path('appointments/accept/<int:pk>/',
         AppointmentAcceptView.as_view(), name='appointment_accept'),

    # url: '/appointments/cancel/', name = core:appointment
    path('appointments/cancel/<int:pk>/',
         AppointmentCancelView.as_view(), name='appointment_cancel'),
]
