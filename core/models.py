from django.db import models
from users.models import User
from django.urls import reverse
from users.appvars import (
    MANAGER, LAWYER, CUSTOMER, USER_TYPE_CHOICES
)


class Appointment(models.Model):

    # related_name is used while querying from a user like
    # user.appointments.all().order_by('-creation_time')
    # As customer and lawyer are pointing to the same tabel, related_name
    # for both of them must be different.
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments")
    lawyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lawyer_appointments")

    # Takes the present time automatically
    creation_time = models.DateTimeField(auto_now_add=True)

    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=500)

    fee = models.IntegerField()

    is_paid = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    NONE = ''
    CANCELLED_BY_CHOICES = [(NONE, 'None')] + USER_TYPE_CHOICES
    cancelled_by = models.CharField(max_length=1, choices=CANCELLED_BY_CHOICES,
                                    default=NONE, verbose_name="Cancelled By")

    @property
    def is_cancelled(self):
        return str(self.cancelled_by) != self.NONE

    @property
    def is_cancelled_by_manager(self):
        return str(self.cancelled_by) == MANAGER

    @property
    def is_cancelled_by_lawyer(self):
        return str(self.cancelled_by) == LAWYER

    @property
    def is_cancelled_by_customer(self):
        return str(self.cancelled_by) == CUSTOMER

    def __str__(self):
        return f'{self.lawyer.username} with {self.customer.username}\
            on {str(self.date)} at {str(self.time)}'

    # Goes to this url after successful creation of an object of this class
    def get_absolute_url(self):
        return reverse('core:appointments')
