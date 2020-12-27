from django import forms
from users.models import LawyerProfile
import datetime as dt


class LawyerProfileForm(forms.ModelForm):

    class Meta:
        model = LawyerProfile
        fields = ['experience', 'categories',
                  'days', 'time_start', 'time_end', 'fee']

        # 2 choices are needed for 2 fields, else both fields will be blank.
        HOUR_CHOICES_1 = [
            (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
        HOUR_CHOICES_2 = [
            (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

        # Customer widget to show hours in the dropdown list.
        widgets = {'time_start': forms.Select(choices=HOUR_CHOICES_1),
                   'time_end': forms.Select(choices=HOUR_CHOICES_2)}
