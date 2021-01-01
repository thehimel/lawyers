from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.decorators import (manager_required)
from django.views.generic import TemplateView


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerDashboardView(TemplateView):

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        user = self.request.user
        context = {
            'msg': 'Only managers can access this page.',
            'name': user.get_full_name,
            'type': user.get_user_type_display,
        }
        return context
