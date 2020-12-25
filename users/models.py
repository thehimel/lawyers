from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from users.appvars import EMPLOYEE, MANAGER


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

    USER_TYPE_CHOICES = [(EMPLOYEE, 'Employee'), (MANAGER, 'Manager'), ]
    GENDER_CHOICES = [('F', 'Female'), ('M', 'Male'), ('O', 'Other'), ]

    # Default user_type must be defined to enforce security
    user_type = models.CharField(max_length=1,
                                 choices=USER_TYPE_CHOICES, default=EMPLOYEE, )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )

    # Using verbose_name in the form.
    pro_pic = models.ImageField(default=user_default_pro_pic,
                                upload_to=user_directory_path,
                                verbose_name="Profile picture")

    # Overriding the save method
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resizing the pro_pic
        resize_img(file_path=self.pro_pic.path, height=300, width=300)

    @property
    def is_employee(self):
        return str(self.user_type) == EMPLOYEE

    @property
    def is_manager(self):
        return str(self.user_type) == MANAGER
