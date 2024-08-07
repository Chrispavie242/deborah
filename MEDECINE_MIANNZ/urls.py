"""
URL configuration for MEDECINE_MIANNZ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from Delice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login/',views.connexion,name='urllogin'),
    path('logout/',views.deconnexion,name='urldeconnexion'),
    path('register/',views.compte,name='urlregister'),

    path('base/',views.base, name='urlbase'),
    path('hom/',views.home, name='urlhome'),

    path('redirection/',views.redirection, name='redirection'),


    path('ajouter_patient/', views.ajouter_patient, name='ajouter_patient'),
    path('liste_patients/', views.liste_patients, name='liste_patients'),

    path('consulter_patient/<int:patient_id>/', views.consulter_patient, name='consulter_patient'),
    path('patients_consultes/', views.patients_consultes, name='patients_consultes'),

    path('hospitaliser_patient/<int:patient_id>/', views.hospitaliser_patient, name='hospitaliser_patient'),
    path('patients_hospitalises/', views.patients_hospitalises, name='patients_hospitalises'),

    path('statut_patient/<int:patient_id>/', views.statut_patient, name='statut_patient'),
    path('modifier_patient/<int:patient_id>/', views.modifier_patient, name='modifier_patient'),
    path('supprimer_patient/<int:patient_id>/', views.supprimer_patient, name='supprimer_patient'),

    path('ajouter_salle/', views.ajouter_salle, name='ajouter_salle'),
    path('liste_salles/', views.liste_salles, name='liste_salles'),
    path('modifier_salles/<int:salle_id>', views.modifier_salles, name='modifier_salles'),
    path('supprimer_salles/<int:salle_id>', views.supprimer_salles, name='supprimer_salles'),

    path('liste_examens/', views.liste_examens, name='liste_examens'),
    path('ajouter_examen/', views.ajouter_examen, name='ajouter_examen'),
    path('modifier_examen/<int:examen_id>', views.modifier_examen, name='modifier_examen'),
    path('supprimer_examen/<int:examen_id>', views.supprimer_examen, name='supprimer_examen'),

    path('liste_laboratoires/', views.liste_laboratoires, name='liste_laboratoires'),
    path('ajouter_laboratoire/', views.ajouter_laboratoire, name='ajouter_laboratoire'),
    path('modifier_laboratoire/<int:laboratoire_id>/', views.modifier_laboratoire, name='modifier_laboratoire'),
    path('supprimer_laboratoire/<int:laboratoire_id>/', views.supprimer_laboratoire, name='supprimer_laboratoire'),

    path('liste_services/', views.liste_services, name='liste_services'),
    path('ajouter_service/', views.ajouter_service, name='ajouter_service'),
    path('modifier_service/<int:service_id>', views.modifier_service, name='modifier_service'),
    path('supprimer_service/<int:service_id>', views.supprimer_service, name='supprimer_service'),

    path('liste_medecins/', views.liste_medecins, name='liste_medecins'),
    path('ajouter_medecin/', views.ajouter_medecin, name='ajouter_medecin'),
    path('modifier_medecin//<int:medecin_id>', views.modifier_medecin, name='modifier_medecin'),
    path('modifier_medecin//<int:medecin_id>', views.supprimer_medecin, name='supprimer_medecin'),



    path('liste_patients_examines/', views.liste_patients_examines, name='liste_patients_examines'),
    path('ajouter_patient_examine/<int:patient_id>/', views.ajouter_patient_examine, name='ajouter_patient_examine'),
     path('modifier_patient_examine/<int:patient_examine_id>/', views.modifier_patient_examine, name='modifier_patient_examine'),
     path('supprimer_patient_examine/<int:patient_examine_id>/', views.supprimer_patient_examine, name='supprimer_patient_examine'),



    path('liste_produits/', views.liste_produits, name='liste_produits'),
    # URL pour ajouter un produit
    path('ajouter_produit/', views.ajouter_produit, name='ajouter_produit'),

    # URL pour supprimer un produit
    path('supprimer_produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),

    # URL pour modifier un produit
    path('modifier_produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),


    # URL pour afficher la liste des ventes des produits
    path('liste_ventes/', views.liste_ventes, name='liste_ventes'),

    path('vendre_produit/<int:produit_id>/', views.vendre_produit, name='vendre_produit'),

    # URL pour effectuer la vente d'un produit
    path('vendre_produit/<int:produit_id>/', views.vendre_produit, name='vendre_produit'),

    # URL pour modifier une vente
    path('modifier_vente/<int:vente_id>/', views.modifier_vente, name='modifier_vente'),

    # URL pour supprimer une vente
    path('supprimer_vente/<int:vente_id>/', views.supprimer_vente, name='supprimer_vente'),

 


]
