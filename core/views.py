from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from users.appvars import EMPLOYEE, MANAGER
from users.decorators import employee_required, manager_required


class HomeView(TemplateView):

    template_name = "core/home.html"


@method_decorator([login_required, employee_required], name='dispatch')
class EmployeeDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only employees can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only managers can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == EMPLOYEE:
            return redirect('core:emp_dashboard')

        elif request.user.user_type == MANAGER:
            return redirect('core:man_dashboard')

    # If user is not authenticated
    return render(request, 'core:home')
