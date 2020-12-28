from django import forms
from core.models import Appointment
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class AppointmentCreateForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'message']

        # Customer widget.
        widgets = {
            # All date formats doesn't work. This one works.
            # https://pypi.org/project/django-bootstrap-datepicker-plus/
            'date': DatePickerInput(format='%Y-%m-%d'),
            'time': TimePickerInput(),
        }
