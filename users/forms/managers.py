from allauth.account.forms import SignupForm
from users.appvars import (
    FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH, MANAGER)
from django import forms


class ManagerSignupForm(SignupForm):

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LENGTH, label='First Name')
    last_name = forms.CharField(
        max_length=LAST_NAME_MAX_LENGTH, label='Last Name')

    def save(self, request):
        user = super(ManagerSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = MANAGER
        user.save()
        return user
