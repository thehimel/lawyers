from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms.common import UserUpdateForm


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
