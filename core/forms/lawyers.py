from django import forms
from users.models import LawyerProfile


class LawyerProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = LawyerProfile
        fields = ['experience', 'categories', 'days', 'fee']
