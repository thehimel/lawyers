from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import (TemplateView, CreateView,
                                  UpdateView, DetailView, ListView)
from users.decorators import (lawyer_required, user_has_address,
                              user_has_no_lawyer_profile)
from core.forms.lawyers import LawyerProfileCreateForm, LawyerProfileUpdateForm
from users.models import LawyerProfile
from core.models import Appointment
from django.contrib import messages


@method_decorator([login_required, lawyer_required], name='dispatch')
class LawyerDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only lawyers can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context


# This is a function, thus it can't redirect the control to another route.
# It can only return True or False.
def valid_office_hours(form, request):
    time_start = form.cleaned_data['time_start']
    time_end = form.cleaned_data['time_end']

    if time_end <= time_start:
        messages.warning(
            request, 'Office hours start time must be smaller than end time.')
        return False

    return True


@method_decorator([login_required, lawyer_required,
                   user_has_address, user_has_no_lawyer_profile],
                  name='dispatch')
class LawyerProfileCreateView(CreateView):
    model = LawyerProfile
    form_class = LawyerProfileCreateForm

    template_name = 'core/lawyer_profile_create.html'

    def form_valid(self, form):
        if not valid_office_hours(form, self.request):
            # Rendering this template with the present form data
            return render(self.request,
                          'core/lawyer_profile_create.html', {'form': form})

        # Selecting the present user as the user of this address
        form.instance.user = self.request.user
        messages.success(self.request, 'Your lawyer profile is created!')
        return super().form_valid(form)


@method_decorator([login_required, lawyer_required,
                   user_has_address], name='dispatch')
class LawyerProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = LawyerProfile
    form_class = LawyerProfileUpdateForm
    template_name = 'core/lawyer_profile.html'

    def test_func(self):
        lawyerprofile = self.get_object()
        # Logged in user must be the owner of the lawyerprofile
        if self.request.user == lawyerprofile.user:
            return True
        return False

    def form_valid(self, form):
        if not valid_office_hours(form, self.request):
            # Rendering this template with the present form data
            return render(self.request,
                          'core/lawyer_profile.html',
                          {'form': form})

        messages.success(self.request, 'Your lawyer profile is updated!')
        return super().form_valid(form)


class LawyerProfileListView(ListView):
    model = LawyerProfile
    template_name = 'core/lawyers.html'
    context_object_name = 'lawyerprofiles'
    # ordering = ['-date_created']
    # paginate_by = 5  # Posts per page


@method_decorator([login_required], name='dispatch')
class LawyerProfileDetailView(DetailView):
    model = LawyerProfile
    context_object_name = 'lawyerprofile'
    template_name = 'core/lawyer.html'


@method_decorator([never_cache, login_required, lawyer_required],
                  name='dispatch')
class AppointmentAcceptView(View):
    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=self.kwargs.get('pk'))

        if appointment.lawyer == request.user:
            if not appointment.is_accepted:
                appointment.is_accepted = True
                appointment.save()
                messages.success(request, 'Appointment accepted.')
            else:
                messages.warning(request, 'Appointment is already accepted.')

        else:
            messages.warning(request, 'Permission denied.')

        return redirect('core:appointments')
