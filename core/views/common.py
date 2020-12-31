from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from users.appvars import LAWYER, CUSTOMER
from users.models import User
from core.models import Appointment
from core.forms.common import AppointmentCreateForm
from core.views.functions import email_appointment_created
from django.contrib import messages


class HomeView(TemplateView):

    template_name = "core/home.html"


def dashboard(request):

    if request.user.is_authenticated:
        if request.user.user_type == LAWYER:
            return redirect('core:lawyer_dashboard')

        elif request.user.user_type == CUSTOMER:
            return redirect('core:customer_dashboard')

    # If user is not authenticated
    return redirect('core:home')


class AppointmentCreateView(LoginRequiredMixin,
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
                if appointment.lawyer == request.user:
                    appointment.is_cancelled_by_lawyer = True

                elif appointment.customer == request.user:
                    appointment.is_cancelled_by_customer = True

                elif request.user.is_manager:
                    appointment.is_cancelled_by_manager = True

                appointment.is_cancelled = True
                appointment.save()
                messages.success(request, 'Appointment cancelled.')
        else:
            messages.warning(request, 'Permission denied.')

        return redirect('core:appointments')
