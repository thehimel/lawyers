from django.db import models
from users.models import User


class Appointment(models.Model):

    # related_name is used while querying from a user like
    # user.appointments.all().order_by('-creation_time')
    # As customer and lawyer are pointing to the same tabel, related_name
    # for both of them must be different.
    customer = models.ManyToManyField(User, related_name='appointments')
    lawyer = models.ManyToManyField(User, related_name='lawyer_appointments')

    # Takes the present time automatically
    creation_time = models.DateTimeField(auto_now_add=True)

    date = models.DateField()
    time = models.TimeField()

    is_paid = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lawyer.get().username} with {self.customer.get().username}\
            on {str(self.date)} at {str(self.time)}'
