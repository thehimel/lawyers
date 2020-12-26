from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.decorators import (lawyer_required, user_has_address,
                              user_has_no_lawyer_profile)
from django.contrib import messages
from allauth.account.views import SignupView
from users.forms.lawyers import LawyerSignupForm
from django.views.generic import CreateView
from users.models import LawyerProfile


# Lawyer Signup View
class LawyerSignupView(SignupView):

    template_name = 'users/signup.html'
    form_class = LawyerSignupForm
    redirect_field_name = 'next'  # Important to redirect user if has next url

    def get_context_data(self, **kwargs):
        ret = super(LawyerSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


@method_decorator([login_required, lawyer_required,
                   user_has_address, user_has_no_lawyer_profile],
                  name='dispatch')
class LawyerProfileCreateView(CreateView):
    model = LawyerProfile
    fields = ['categories', 'days', 'consultation_fee']

    template_name = 'users/lawyer.html'

    def form_valid(self, form):
        # Selecting the present user as the user of this address
        form.instance.user = self.request.user
        messages.success(self.request, 'Your lawyer profile is created!')
        return super().form_valid(form)
