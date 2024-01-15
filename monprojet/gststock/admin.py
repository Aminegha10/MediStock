from django.contrib import admin

# Register your models here.
from .models import medicament,Notification
admin.site.register(medicament)
admin.site.register(Notification)