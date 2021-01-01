from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.mixins import NotLawyerMixin
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from users.appvars import MANAGER, LAWYER, CUSTOMER
from core.appvars import APPOINTMENT_DATE_MAX_LIMIT_IN_DAYS
from users.models import User
from core.models import Appointment
from core.forms.common import AppointmentCreateForm
from core.views.functions import email_appointment_created
from django.contrib import messages
from datetime import date


class HomeView(TemplateView):

    template_name = "core/home.html"


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == MANAGER:
            return redirect('core:manager_dashboard')

        if request.user.user_type == LAWYER:
            return redirect('core:lawyer_dashboard')

        elif request.user.user_type == CUSTOMER:
            return redirect('core:customer_dashboard')

    # If user is not authenticated
    return redirect('core:home')


# This is a function, thus it can't redirect the control to another route.
# It can only return True or False.
def valid_date_time(form, request, lawyer):
    time_start = lawyer.lawyerprofile.time_start
    time_end = lawyer.lawyerprofile.time_end
    appointment_date = form.cleaned_data['date']
    time = form.cleaned_data['time']

    is_valid = True

    today = date.today()
    limit = APPOINTMENT_DATE_MAX_LIMIT_IN_DAYS

    if appointment_date < today:
        messages.warning(
            request, 'Appointment date can not be in past.')
        is_valid = False

    if abs((appointment_date - today).days) > limit:
        messages.warning(
            request, f'Appointment date must be within next {limit} days.')
        is_valid = False

    # If we display only str(time_start), it shows like 14:20:00.
    # Thus, we are taking only first 5 characters to display 14:20.
    if time < time_start or time > time_end:
        messages.warning(
            request, f'Appointment time must be between \
                {str(time_start)[:5]} and {str(time_end)[:5]}.')
        is_valid = False

    return is_valid


# One lawyer can't book appointment for another lawyer
# Customers and managers can book appointment.
class AppointmentCreateView(LoginRequiredMixin, NotLawyerMixin,
                            UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm

    template_name = 'core/appointment.html'

    def test_func(self):
        pk = self.kwargs['pk']

        # Selecting the user with the pk as the lawyer
        lawyer = User.objects.get(pk=pk)
        customer = self.request.user

        # Check whether the lawyer has a lawyer profile or not.
        # Check lawyer and customer are same or not.
        if hasattr(lawyer, 'lawyerprofile') and lawyer != customer:
            return True
        return False

    def form_valid(self, form):
        # We have accepted a value as pk in the url.
        pk = self.kwargs['pk']

        # Selecting the user with the pk as the lawyer
        lawyer = User.objects.get(pk=pk)
        if not valid_date_time(form, self.request, lawyer):
            # Rendering this template with the present form data
            return render(self.request,
                          'core/appointment.html', {'form': form})

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
            email_appointment_created(customer, lawyer, form.instance)

        # If the email is not sent, just proceed.
        except Exception:
            pass

        return super().form_valid(form)


# For customer
class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'core/appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Returning the user if exists else 404
        user = self.request.user

        if user.is_customer:
            # All appointments of customer user with descending date ordering
            return Appointment.objects.filter(
                customer=user).order_by('-creation_time')

        elif user.is_lawyer:
            return Appointment.objects.filter(
                lawyer=user).order_by('-creation_time')

        elif user.is_manager:
            return Appointment.objects.all().order_by('-creation_time')


@method_decorator([never_cache, login_required], name='dispatch')
class AppointmentCancelView(View):
    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=self.kwargs.get('pk'))

        if (request.user == appointment.lawyer or
            request.user == appointment.customer or
                request.user.is_manager):

            if appointment.is_cancelled:
                messages.warning(request, 'Appointment is already cancelled.')

            else:
                if request.user.is_manager:
                    appointment.cancelled_by = MANAGER

                elif appointment.lawyer == request.user:
                    appointment.cancelled_by = LAWYER

                elif appointment.customer == request.user:
                    appointment.cancelled_by = CUSTOMER

                appointment.save()
                messages.success(request, 'Appointment cancelled.')
        else:
            messages.warning(request, 'Permission denied.')

        # Redirect to previous page
        return redirect(request.META.get('HTTP_REFERER', '/'))
