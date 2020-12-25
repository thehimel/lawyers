from allauth.account.views import SignupView
from users.forms.lawyers import LawyerSignupForm


# Lawyer Signup View
class LawyerSignupView(SignupView):

    template_name = 'users/signup.html'
    form_class = LawyerSignupForm
    redirect_field_name = 'next'  # Important to redirect user if has next url

    def get_context_data(self, **kwargs):
        ret = super(LawyerSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret
