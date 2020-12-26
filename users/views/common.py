from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from users.forms.common import UserUpdateForm, AddressUpdateForm
from users.models import Address


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
              'street', 'city', 'state', 'country']

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
                messages.success(request, 'Your address has been updated!')
                return redirect('users:profile')

        # If it's not POST, it's GET. Thus generate the form.
        else:
            form = AddressUpdateForm(instance=request.user.address)

        context = {
            'form': form,
        }

        return render(request, 'users/address.html', context)

    # If the user doesn't have any address
    except Exception:
        messages.warning(
            request, 'You must create an address first to update it.')
        return redirect('users:profile')
