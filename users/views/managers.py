from allauth.account.views import SignupView
from users.forms.managers import ManagerSignupForm


# Manager Signup View
class ManagerSignupView(SignupView):

    template_name = 'users/signup.html'
    form_class = ManagerSignupForm
    redirect_field_name = 'next'  # Important to redirect user if has next url

    def get_context_data(self, **kwargs):
        ret = super(ManagerSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret
