from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from users.forms.common import UserUpdateForm
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
