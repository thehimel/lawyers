from django import forms
from users.models import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'gender', 'categories', 'pro_pic']

        # If you want to change the lebel of any field in the form.
        # labels = {
        #     "first_name": "First Name",
        #     "last_name": "Last Name"
        # }
