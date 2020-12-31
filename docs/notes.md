# Notes

## File Size and Content Type Validations
- [Resource](https://stackoverflow.com/questions/2472422/django-file-upload-size-limit)

## Sending Email with Django:
- [General](https://data-flair.training/blogs/django-send-email/)
- [Customize Display Name](https://stackoverflow.com/questions/2111452/giving-email-account-a-name-when-sending-emails-with-django-through-google-apps)
- [HTML Email](https://stackoverflow.com/questions/3005080/how-to-send-html-email-with-django-with-dynamic-content-in-it)
- [Include BCC and CC](https://stackoverflow.com/questions/17064497/send-email-to-bcc-and-cc-in-django)
- [Django Email Doc](https://docs.djangoproject.com/en/1.10/topics/email/)

## Date and Time
- [Python Date Time Format](https://www.programiz.com/python-programming/datetime/strptime)
- [Python Date Time Format Examples](https://stackoverflow.com/questions/34639280/how-to-display-django-time-in-12-hour-time-instead-of-military-24)
- [Django Template Time Formats](https://docs.djangoproject.com/en/dev/ref/templates/builtins/?from=olddocs#now)
- [Django Template Time with 12 Hour Format and Lowercase](https://stackoverflow.com/questions/12218620/in-django-how-to-display-times-with-lowercase-am-pm-in-templates)
- {{ form_data.date|date:'d/m/Y' }} shows date as 30/12/2020 and {{ form_data.date|date:'d-m-Y' }} shows date as 30-12-2020.
- {{ form_data.time|date:'H:i' }} shows date as 14:20.
- {{ form_data.time|date:'g:i A' }} shows date as 02:20 PM and {{ form_data.time|date:'g:i A'|lower }} shows date as 02:20 pm.
- {% now "d-m-Y g:i A" %} shows current time as 30-12-2020 02:20 PM

## Customer Widget for Time Picker
```python
# Only difference is user can't update the document.
class LawyerProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = LawyerProfile
        fields = ['about', 'experience', 'categories',
                  'days', 'time_start', 'time_end', 'fee']

        # 2 choices are needed for 2 fields, else both fields will be blank.
        HOUR_CHOICES_1 = [
            (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
        HOUR_CHOICES_2 = [
            (dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

        # Customer widget to show hours in the dropdown list.
        widgets = {'time_start': forms.Select(choices=HOUR_CHOICES_1),
                   'time_end': forms.Select(choices=HOUR_CHOICES_2)}
```