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

## [Redirect to Previous Page](https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request/35796330)

```python
# Redirect to previous page
return redirect(request.META.get('HTTP_REFERER', '/'))
```

## [Redirect to 'next'](https://stackoverflow.com/questions/38431166/redirect-to-next-after-login-in-django)
```python
# Simple
return redirect(self.request.GET.get('next'))

# For UpdateVIew()

def form_valid(self, form):

        # Your additional code to perform anything

        # If the 'next' exists and it is save, we update the success_url.
        # If the 'next'is doesn't exists or it is not a save url,
        # by default the success_url is the source of the request.
        next_url = self.request.GET.get("next", None)
        if next_url and is_safe_url(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure()):

            self.success_url = next_url

        return super().form_valid(form)

# For General
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.conf import settings

def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not is_safe_url(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)

def my_login_view(request):
    # TODO: Check if its ok to login.
    # Then either safely redirect og go to default startpage.
    return redirect_after_login(request)
```

## [Difference Between 2 Dates in Python](https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python)

## [Django Template View for Empty List](https://stackoverflow.com/questions/902034/how-can-i-check-the-size-of-a-collection-within-a-django-template)

## [Bootstrap 4 Sticky Footer](https://stackoverflow.com/questions/46722697/bootstrap-4-sticky-footer-not-sticking)

```html
<div class="d-flex flex-column min-vh-100">
    <nav>
    </nav>
    <main class="flex-fill">
    </main>
    <footer>
    </footer>
</div>
```

## Resize and Crop Image Before Uploading
- [Resize Image before Uploading](https://stackoverflow.com/questions/52183975/how-to-compress-the-image-before-uploading-to-s3-in-django)
- [Compress Image before Uploading](https://dev.to/gajesh/compress-images-in-django-3la8)
- [Crop Image from Center to Make It Square](https://stackoverflow.com/questions/54545621/how-to-resize-and-crop-an-image-into-a-square-in-django)


## [Get and Set Attribute of an Object from String](https://stackoverflow.com/questions/3253966/python-string-to-attribute)

```python
# If someobject has an attribute named foostring then
def get_foo(someobject, foostring):
    return getattr(someobject, foostring)

# or if you want to set an attribute to the supplied object then:
def set_foo(someobject, foostring, value):
    return setattr(someobject,foostring, value)
```

## Django 'File' object has no attribute 'content_type'
- [Discussion](https://stackoverflow.com/questions/22397637/django-file-object-has-no-attribute-content-type)

```python
#DJANGO_TYPE = self.image.file.content_type

if self.image.name.endswith(".jpg"):
    PIL_TYPE = 'jpeg'
    FILE_EXTENSION = 'jpg'
    DJANGO_TYPE = 'image/jpeg'

elif self.image.name.endswith(".png"):
    PIL_TYPE = 'png'
    FILE_EXTENSION = 'png'
    DJANGO_TYPE = 'image/png'
```


## [django-money](https://pypi.org/project/django-money/)

- Allowed Currencies

```python
# settings.py
CURRENCIES = ('USD', 'EUR', 'INR', 'BDT')
```


## Add Classes to Existing CLass with Crispy Forms

```python
# settings.py
CRISPY_CLASS_CONVERTERS = {
    'numberinput': 'numberinput form-control',
    'select': 'select form-control'
}
```

```html
<input type="number" name="fee_0" step="0.01" class="numberinput form-control" required="" id="id_fee_0">
<select name="fee_1" class="select" required id="id_fee_1">
    <option value="EUR" selected>Euro</option>
    <option value="INR">Indian Rupee</option>
    <option value="BDT">Taka</option>
    <option value="USD">US Dollar</option>
</select>
```

## Showing Errors for django-money Fields in the Template

```html
{# django-money fields doesn't show errors, thus showing the error manually. #}
{% if form.errors %}
    {% for error in form.fee.errors %}
    <div class="text-center alert alert-dismissible fade show alert-{% if messages.tags %}{{ message.tags }}{% else %}info{% endif %}"
        role="alert">

        {{error}}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>

    </div>
    {% endfor %}
{% endif %}
```

## Pass Argument to a View after Object Creation

```python
class LawyerProfile(models.Model):
    # Your Code
    def get_absolute_url(self):  # new
        return reverse('core:lawyer_profile', kwargs={'pk': self.pk})
```