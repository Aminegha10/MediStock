from django.contrib import admin

# Register your models here.
from .models import Facture,MedicamentsFacture
admin.site.register(Facture)
admin.site.register(MedicamentsFacture)