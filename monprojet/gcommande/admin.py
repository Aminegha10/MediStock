from django.contrib import admin

# Register your models here.
from .models import gcommandes,MedicamentsCommande
admin.site.register(gcommandes)
admin.site.register(MedicamentsCommande)