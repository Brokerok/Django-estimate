from django.contrib import admin
from .models import User, Pdf, Order

admin.site.register(User)
admin.site.register(Pdf)
admin.site.register(Order)
