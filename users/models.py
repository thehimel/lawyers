from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
from users.appvars import (
    MANAGER, LAWYER, CUSTOMER, USER_TYPE_CHOICES,
    FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH,
    CATEGORY_MAX_LENGTH
)
from users.functions import resize_image, file_size


user_default_pro_pic = 'img/defaults/user_pro_pic.jpg'

# https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.FileField.upload_to


def user_dir(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/{1}'.format(instance.id, filename)


# For lawyer profile, we get the user_id from instance.user.id
def user_dir_lawyer_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/{1}'.format(instance.user.id, filename)


# Fields provided by default
# username, first_name, last_name, email, password
# is_staff, is_active, is_superuser, date_joined, last_login
class User(AbstractUser):
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH, verbose_name="First Name")
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH, verbose_name="Last Name")

    # The first option is kept empty, to show the corresponding text as
    # the first option in the dropdown
    GENDER_CHOICES = [('', 'Select'), ('F', 'Female'),
                      ('M', 'Male'), ('O', 'Other')]

    # Default user_type must be defined to enforce security
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES,
                                 default=CUSTOMER, verbose_name="User Type")

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )

    # Using verbose_name in the form.
    pro_pic = models.ImageField(default=user_default_pro_pic,
                                upload_to=user_dir,
                                verbose_name="Profile Picture",
                                validators=[file_size])

    # Overriding the save method
    def save(self, *args, **kwargs):
        # Resize image before upload.
        resize_image(form_data=self, field_name='pro_pic')
        super().save(*args, **kwargs)

    @property
    def is_manager(self):
        return str(self.user_type) == MANAGER

    @property
    def is_lawyer(self):
        return str(self.user_type) == LAWYER

    @property
    def is_customer(self):
        return str(self.user_type) == CUSTOMER

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    flat_number = models.CharField(
        max_length=10, blank=True, verbose_name="Flat Number")
    apartment_number = models.CharField(
        max_length=10, blank=True, verbose_name="Apartment Number")

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)

    # blank_label is being used to show as the first option in the dropdown
    country = CountryField(blank_label='Select')

    def __str__(self):
        return (self.flat_number + ', ' + self.street + ' ' +
                self.apartment_number + ', ' + self.city + ', ' +
                self.state + ', ' + str(self.country))

    # Goes to this url after successful creation of an object of this class
    def get_absolute_url(self):
        return reverse('users:profile')


class Category(models.Model):
    name = models.CharField(max_length=CATEGORY_MAX_LENGTH)

    def __str__(self):
        return self.name


class LawyerProfile(models.Model):

    # Every lawyer can have only one lawyer profile.
    # When user is deleted, lawyer profile will be deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=500)
    experience = models.IntegerField(verbose_name="Experience in Year")

    # LawyerProfile-Category has many-to-many relationship.
    # multiple lawyers can have multiple categories.
    # if category is deleted, user will not be deleted bydefault.
    categories = models.ManyToManyField(Category)

    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    days = MultiSelectField(choices=DAYS_OF_WEEK,
                            max_choices=6, verbose_name="Working Days")

    time_start = models.TimeField(verbose_name="Office Hours Start")
    time_end = models.TimeField(verbose_name="Office Hours End")

    fee = models.IntegerField(verbose_name="Consultation Fee")

    # As we are using Cloudary for media storage, we can't server pdf for free
    # Thus, we are defining this field as ImageField()
    # document = models.FileField(upload_to=user_dir_lawyer_profile,
    #                             verbose_name="Official Document",
    #                             validators=[file_size, content_type_pdf])

    document = models.ImageField(upload_to=user_dir_lawyer_profile,
                                 verbose_name="Official Document",
                                 validators=[file_size])

    is_verified = models.BooleanField(default=False)

    # Overriding the save method
    def save(self, *args, **kwargs):
        # Resize image before upload.
        resize_image(form_data=self, field_name='document',
                     height_limit=1200, square=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):  # new
        return reverse('core:lawyer_profile')
