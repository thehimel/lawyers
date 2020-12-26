from django.contrib import admin
from users.models import User, Category, Address, LawyerProfile

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(LawyerProfile)
