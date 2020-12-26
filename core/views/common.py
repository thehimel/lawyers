from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from users.appvars import LAWYER, CUSTOMER


class HomeView(TemplateView):

    template_name = "core/home.html"


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == LAWYER:
            return redirect('core:lawyer_dashboard')

        elif request.user.user_type == CUSTOMER:
            return redirect('core:customer_dashboard')

    # If user is not authenticated
    return render(request, 'core:home')
