from django import forms
from core.models import Appointment
import datetime as dt


class AppointmentCreateForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'message']

        HOUR_CHOICES = [
            (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

        # Customer widget to show hours in the dropdown list.
        widgets = {
            'time': forms.Select(choices=HOUR_CHOICES)
        }
