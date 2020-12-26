from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView
from users.decorators import (lawyer_required, user_has_address,
                              user_has_no_lawyer_profile)
from users.models import LawyerProfile
from django.contrib import messages


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


@method_decorator([login_required, lawyer_required,
                   user_has_address, user_has_no_lawyer_profile],
                  name='dispatch')
class LawyerProfileCreateView(CreateView):
    model = LawyerProfile
    fields = ['categories', 'days', 'consultation_fee']

    template_name = 'core/lawyer_profile_create.html'

    def form_valid(self, form):
        # Selecting the present user as the user of this address
        form.instance.user = self.request.user
        messages.success(self.request, 'Your lawyer profile is created!')
        return super().form_valid(form)
