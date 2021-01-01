from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from users.decorators import manager_required
from users.models import LawyerProfile
from django.contrib import messages


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


@method_decorator([never_cache, login_required, manager_required],
                  name='dispatch')
class VerifyLawyerProfileView(View):
    def get(self, request, *args, **kwargs):
        lawyerprofile = get_object_or_404(
            LawyerProfile, pk=self.kwargs.get('pk'))

        if lawyerprofile.is_verified:
            messages.warning(request, 'Lawyer is already verified.')

        else:
            lawyerprofile.is_verified = True
            lawyerprofile.save()
            messages.success(request, 'Lawyer verification successful.')

        # Redirect to previous page
        return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator([never_cache, login_required, manager_required],
                  name='dispatch')
class UnverifyLawyerProfileView(View):
    def get(self, request, *args, **kwargs):
        lawyerprofile = get_object_or_404(
            LawyerProfile, pk=self.kwargs.get('pk'))

        if not lawyerprofile.is_verified:
            messages.warning(request, 'Lawyer is not yet verified.')

        else:
            lawyerprofile.is_verified = False
            lawyerprofile.save()
            messages.success(request, 'Lawyer unverified successfully.')

        # Redirect to previous page
        return redirect(request.META.get('HTTP_REFERER', '/'))
