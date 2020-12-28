from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, ListView
from users.appvars import LAWYER, CUSTOMER
from core.models import Appointment
from core.forms.common import AppointmentCreateForm
from users.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class HomeView(TemplateView):

    template_name = "core/home.html"


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == LAWYER:
            return redirect('core:lawyer_dashboard')

        elif request.user.user_type == CUSTOMER:
            return redirect('core:customer_dashboard')

    # If user is not authenticated
    return render(request, 'core:home')


def email_created(customer, lawyer, form_data):
    subject = 'Appointment Booking Confirmation'

    # This format must be followed to show Lawyers as the display name.
    # The email inside the <> will be replaced with the actual email.
    sender_name = 'Lawyers <noreply@domain.com>'

    recipients = [customer.email, lawyer.email]

    template_name = 'core/email/appointment_created.html'
    context = {
        'customer': customer,
        'lawyer': lawyer,
        'form_data': form_data,
    }

    # render with dynamic value
    html_content = render_to_string(template_name, context)

    # Strip the html tag. So people can see the pure text at least.
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, sender_name,
                                 recipients, fail_silently=False)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class AppointmentCreateView(LoginRequiredMixin,
                            UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm

    template_name = 'core/appointment.html'

    def test_func(self):
        pk = self.kwargs['pk']

        # Selecting the user with the pk as the lawyer
        lawyer = User.objects.get(pk=pk)

        # Check whether the lawyer has a lawyer profile or not.
        # It is possible that the lawyer doesn't have any lawyerprofile
        # object. Thus use try and except to stay safe.
        try:
            if lawyer.lawyerprofile:
                return True
        except Exception:
            return False

    def form_valid(self, form):
        # We have accepted a value as pk in the url.
        pk = self.kwargs['pk']

        # Selecting the user with the pk as the lawyer
        lawyer = User.objects.get(pk=pk)
        form.instance.lawyer = User.objects.get(pk=pk)

        # Saving the fee of the lawyer as the fee of this appointment
        form.instance.fee = lawyer.lawyerprofile.fee

        # Selecting the present user as the customer
        customer = self.request.user
        form.instance.customer = customer
        messages.success(self.request, 'Appointment is booked successfully.')

        # Sending email may fail.
        # Using try and except to always save the object.
        try:
            email_created(customer, lawyer, form.instance)

        # If the email is not sent, just proceed.
        except Exception:
            pass

        return super().form_valid(form)


# For customer
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'core/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Returning the user if exists else 404
        user = self.request.user

        # Returning all posts by that user with descending (-ve) date ordering
        return Appointment.objects.filter(
            customer=user).order_by('-creation_time')
