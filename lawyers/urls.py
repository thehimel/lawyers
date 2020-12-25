"""Example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # With the default signup url, users can register without user_type.
    # In our User model, we've declared EMPLOYEE as the default user_type.
    # With this we avoid the security concern here. But we don't want to let
    # the user register without some extra fields like First/Last Name etc.
    # It's very important to exclude the default allauth signup url.
    # Name for this url is account_signup and if we redefine the url
    # to page_not_found, no one will be able to access this path.
    # While using page_not_found, kwargs must be used with defined exception.
    # path('accounts/signup', page_not_found,
    #      kwargs={'exception': Exception('Page not Found')}),
    # We may also use RedirectView and redirect the user to users:emp_signup.

    path('accounts/signup',
         RedirectView.as_view(
             pattern_name='users:emp_signup', permanent=False)),

    path('users/', include('users.urls', namespace='users')),
    path('', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    import debug_toolbar

    # For Django Debug Toolbar in debug mode.
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    # To serve static files in debug mode
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    # To serve media files in debug mode
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
