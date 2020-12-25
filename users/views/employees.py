from allauth.account.views import SignupView
from users.forms.employees import EmployeeSignupForm


# Employee Signup View
class EmployeeSignupView(SignupView):

    template_name = 'users/signup.html'  # Custom template is mandatory
    form_class = EmployeeSignupForm
    redirect_field_name = 'next'  # Important to redirect user if has next url

    # This is mandatory and copy-pasted
    def get_context_data(self, **kwargs):
        ret = super(EmployeeSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret
