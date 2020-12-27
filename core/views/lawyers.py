from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from users.decorators import (lawyer_required, user_has_address,
                              user_has_no_lawyer_profile)
from core.forms.lawyers import LawyerProfileCreateForm, LawyerProfileUpdateForm
from users.models import LawyerProfile
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


# We are using function based view for update because
# in class based update view, pk must be passed.
# But we don't want to disclose the pk of an object.
# With function based view, we take the instance from the request.
def lawyer_profile_update(request):
    try:
        # If the user has a lawyer profile, do the following.
        request.user.lawyerprofile is not None

        if request.method == 'POST':
            form = LawyerProfileUpdateForm(
                request.POST, instance=request.user.lawyerprofile)
            if form.is_valid():
                if not valid_office_hours(form, request):
                    # Rendering this template with the present form data
                    return render(request,
                                  'core/lawyer_profile.html',
                                  {'form': form})

                form.save()
                messages.success(request, 'Your lawyer profile is updated!')
                return redirect('core:lawyer_profile')

        # If it's not POST, it's GET. Thus generate the form.
        else:
            form = LawyerProfileUpdateForm(instance=request.user.lawyerprofile)
            context = {'form': form}
            return render(request, 'core/lawyer_profile.html', context)

    # If the user doesn't have any lawyer profile
    except Exception:
        messages.warning(
            request, 'You must create a lawyer profile first to update it.')
        return redirect('core:lawyer_profile_create')


class LawyerProfileListView(ListView):
    model = LawyerProfile
    template_name = 'core/lawyers.html'
    context_object_name = 'lawyerprofiles'
    # ordering = ['-date_created']
    # paginate_by = 5  # Posts per page
