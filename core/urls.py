from django.urls import path
from core.views import (
    HomeView, CustomerDashboardView, LawyerDashboardView, dashboard
)

app_name = 'core'

urlpatterns = [
    # url: '/', name = core:home
    path('', HomeView.as_view(), name='home'),

    # url: '/customers/dashboard', name = core:customer_dashboard
    path('customers/dashboard',
         CustomerDashboardView.as_view(), name='customer_dashboard'),

    # url: '/lawyers/dashboard', name = core:lawyer_dashboard
    path('lawyers/dashboard',
         LawyerDashboardView.as_view(), name='lawyer_dashboard'),

    # url: '/dashboard', name = core:dashboard
    path('dashboard/', dashboard, name='dashboard'),
]
