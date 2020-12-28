from django import forms
from users.models import LawyerProfile
from bootstrap_datepicker_plus import TimePickerInput


class LawyerProfileCreateForm(forms.ModelForm):

    class Meta:
        model = LawyerProfile
        fields = ['about', 'experience', 'categories',
                  'days', 'time_start', 'time_end', 'fee', 'document']

        # Customer widget.
        widgets = {
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }


# Only difference is user can't update the document.
class LawyerProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = LawyerProfile
        fields = ['about', 'experience', 'categories',
                  'days', 'time_start', 'time_end', 'fee']

        # Customer widget.
        widgets = {
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }
