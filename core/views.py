from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from users.appvars import LAWYER, CUSTOMER
from users.decorators import lawyer_required, customer_required


class HomeView(TemplateView):

    template_name = "core/home.html"


@method_decorator([login_required, lawyer_required], name='dispatch')
class LawyerDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only lawyers can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context


@method_decorator([login_required, customer_required], name='dispatch')
class CustomerDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only customers can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == LAWYER:
            return redirect('core:lawyer_dashboard')

        elif request.user.user_type == CUSTOMER:
            return redirect('core:customer_dashboard')

    # If user is not authenticated
    return render(request, 'core:home')
