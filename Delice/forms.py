from django import forms
from .models import Hospitalisation, Consultation, Patient, Salle, Examen, Laboratoire, Service, Medecin, PatientExamine, Produit, Vente
from django.contrib.auth.models import User


class HospitalisationForm(forms.ModelForm):
    class Meta:
        model = Hospitalisation
        fields = ['salle']


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['montant_pour_consultation', 'avis_du_medecin']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'ce_que_vous_ressenter', 'mail', 'portable']

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom']  # Ajoutez d'autres champs si nécessaire

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nom', 'desciption']

class LaboratoireForm(forms.ModelForm):
    class Meta:
        model = Laboratoire
        fields = ['nom_laboratoire', 'desciption_labo']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom_service', 'labo_requis']

class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom_medecin', 'prenom_medecin', 'service']

class PatientExamineForm(forms.ModelForm):
    class Meta:
        model = PatientExamine
        fields = ['patient', 'examen', 'nom_du_labo']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'prix_unitaire', 'quantite_stock']

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['produit','quantite_vendue', 'vendeur']