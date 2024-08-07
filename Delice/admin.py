from django.contrib import admin
from .models import Salle, Patient, Consultation, Hospitalisation, Examen, PatientExamine, Produit, Vente, Laboratoire, Medecin,Service

# Register your models here.
admin.site.register(Patient)
admin.site.register(Salle)
admin.site.register(Consultation)
admin.site.register(Hospitalisation)
admin.site.register(Examen)
admin.site.register(PatientExamine)
admin.site.register(Produit)
admin.site.register(Vente)
admin.site.register(Laboratoire)
admin.site.register(Medecin)
admin.site.register(Service)