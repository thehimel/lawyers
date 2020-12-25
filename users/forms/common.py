from django import forms
from users.models import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender', 'pro_pic', ]
