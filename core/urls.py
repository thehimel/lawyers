from django.urls import path
from core.views import (
    HomeView, EmployeeDashboardView, ManagerDashboardView, dashboard
)

app_name = 'core'

urlpatterns = [
    # url: '/', name = core:home
    path('', HomeView.as_view(), name='home'),

    # url: '/employees/dashboard', name = core:emp_dashboard
    path('employees/dashboard',
         EmployeeDashboardView.as_view(), name='emp_dashboard'),

    # url: '/managers/dashboard', name = core:man_dashboard
    path('managers/dashboard',
         ManagerDashboardView.as_view(), name='man_dashboard'),

    # url: '/dashboard', name = core:dashboard
    path('dashboard/', dashboard, name='dashboard'),
]
