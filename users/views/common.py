from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from users.forms.common import UserUpdateForm, AddressUpdateForm
from users.models import Address
from django.utils.http import is_safe_url


# Common Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile')

    # If it's not POST, it's GET. Thus generate the form.
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'users/profile.html', context)


class AddressCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Address
    fields = ['flat_number', 'apartment_number',
              'street', 'city', 'state', 'postal_code', 'country']

    template_name = 'users/address.html'

    def test_func(self):
        try:
            # If the user has an address, return False.
            self.request.user.address is not None
            return False
        except Exception:
            return True

    def form_valid(self, form):
        # Selecting the present user as the user of this address
        form.instance.user = self.request.user
        messages.success(self.request, 'Your address is created!')

        # To create a lawyer profile, or to book an appointment,
        # it is mandatory to have an address. While performing these
        # tasks, if the user doesn't have an address. User will be redirected
        # to AddressCreateView() with a 'next' parameter.
        # If the 'next' exists and it is save, we update the success_url.
        # If the 'next'is doesn't exists or it is not a save url,
        # by default the success_url is the source of the request.
        next_url = self.request.GET.get("next", None)
        if next_url and is_safe_url(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure()):

            self.success_url = next_url

        return super().form_valid(form)


@login_required
def address_update(request):
    try:
        # If the user has an address, do the following.
        request.user.address is not None

        if request.method == 'POST':
            form = AddressUpdateForm(
                request.POST, instance=request.user.address)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your address is updated!')
                return redirect('users:profile')

        # If it's not POST, it's GET. Thus generate the form.
        else:
            form = AddressUpdateForm(instance=request.user.address)

            context = {'form': form}

            return render(request, 'users/address.html', context)

    # If the user doesn't have any address
    except Exception:
        messages.warning(
            request, 'You must create an address first to update it.')
        return redirect('users:profile')
