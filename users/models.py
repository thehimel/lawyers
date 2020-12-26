from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.urls import reverse
from multiselectfield import MultiSelectField
from users.appvars import (
    MANAGER, LAWYER, CUSTOMER, FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH, CATEGORY_MAX_LENGTH
)


user_default_pro_pic = 'img/defaults/user_pro_pic.jpg'


def resize_img(file_path, height=300, width=300):
    """ Resize an image. file_path, height and width to set is passed. """
    img = Image.open(file_path)
    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)
        img.save(file_path)


# https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.FileField.upload_to
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/{1}'.format(instance.id, filename)


# Fields provided by default
# username, first_name, last_name, email, password
# is_staff, is_active, is_superuser, date_joined, last_login
class User(AbstractUser):
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH, verbose_name="First Name")
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH, verbose_name="Last Name")

    USER_TYPE_CHOICES = [(MANAGER, 'Manager'),
                         (LAWYER, 'Lawyer'), (CUSTOMER, 'Customer')]

    GENDER_CHOICES = [('F', 'Female'), ('M', 'Male'), ('O', 'Other')]

    # Default user_type must be defined to enforce security
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES,
                                 default=CUSTOMER, verbose_name="User Type")

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )

    # Using verbose_name in the form.
    pro_pic = models.ImageField(default=user_default_pro_pic,
                                upload_to=user_directory_path,
                                verbose_name="Profile Picture")

    # Overriding the save method
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resizing the pro_pic
        resize_img(file_path=self.pro_pic.path, height=300, width=300)

    @property
    def is_manager(self):
        return str(self.user_type) == MANAGER

    @property
    def is_lawyer(self):
        return str(self.user_type) == LAWYER

    @property
    def is_customer(self):
        return str(self.user_type) == CUSTOMER


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    flat_number = models.CharField(
        max_length=10, blank=True, verbose_name="Flat Numnber")
    apartment_number = models.CharField(
        max_length=10, blank=True, verbose_name="Apartment Numnber")

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return (self.flat_number + ', ' + self.street + ' ' +
                self.apartment_number + ', ' + self.city + ', ' +
                self.state + ', ' + self.country)

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

    consultation_fee = models.IntegerField(verbose_name="Consultation Fee")

    def __str__(self):
        return self.user.username
