from users.appvars import LAWYER
from django.shortcuts import redirect
from django.contrib import messages


class NotLawyerMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != LAWYER:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, 'One lawyer can not book appointment\
                     for another lawyer.')
            return redirect('core:appointments')
