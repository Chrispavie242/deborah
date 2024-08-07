from django.shortcuts import render,redirect,get_object_or_404
from .models import Patient, Hospitalisation, Salle, Examen, Laboratoire, Service, Medecin, PatientExamine, Produit, Vente, Consultation
from .forms import HospitalisationForm, ConsultationForm, PatientForm, SalleForm, ExamenForm, LaboratoireForm, ServiceForm, MedecinForm, PatientExamineForm, ProduitForm, VenteForm
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import make_aware, is_naive

from django.urls import reverse


from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Sum, F
from django.utils.timezone import now
from decimal import Decimal

from django.db.models import F, ExpressionWrapper, DecimalField


def base(request):
    return render(request,'base.html')

def home(request):
    if request.method=="POST":
        valeur=request.POST
        #recuperation des valeurs saisies au formulaire
        nom=valeur.get('nom')
        prenom=valeur.get('prenom')
        ce_que_vous_ressenter=valeur.get('ce_que_vous_ressenter')
        mail=valeur.get('mail')
        portable=valeur.get('portable')

        #enregistrer les informations dans la table ou encore base de données
        data=Patient.objects.create(nom=nom, prenom=prenom, ce_que_vous_ressenter=ce_que_vous_ressenter, mail=mail, portable=portable)
    return render(request,'home.html')


def compte(request):
    if request.method=="POST":
        data = request.POST
        if data.get('password1') == data.get('password'):
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            isinstance = User.objects.create_user(username=username, email=email, password=password)
            print("compte crée avec succès")
        else:
            print("le compte n'a pas été créé")
    return render(request,'register.html')


def connexion(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user: #si les données que l'utilisateur a saisie est identique à celle se trouvant dans la base de donner
            login(request, user) #permet à la personne de se connecter à l'application
            print("connexion réussie")
            return redirect('redirection') #renvoyer l'utilisateur à la page d'accueil une fois connecté
    return render(request,'login.html')


def deconnexion(request):
    logout(request)
    print("deconnexion réussie")
    return redirect('urllogin')




@login_required(login_url='urllogin')
def liste_patients(request):
    patients = Patient.objects.all()
    return render(request, 'liste_patients.html', {'patients': patients})


@login_required(login_url='urllogin')
def redirection(request):
    return render(request, 'redirection.html')


#Cette vue nous permet de consulter  un patient
@login_required(login_url='urllogin')
def consulter_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            return redirect('liste_patients')
    else:
        form = ConsultationForm()
    return render(request, 'consulter_patients.html', {'patient': patient, 'form': form})

#cette vue nous permet d'afficher les patients consultés
@login_required(login_url='urllogin')
def patients_consultes(request):
    patients_consultes = Consultation.objects.all()
    return render(request, 'liste_patients_consultes.html', {'patients_consultes': patients_consultes})



#Cette vue nous permet d'hospitaliser un patient
@login_required(login_url='urllogin')
def hospitaliser_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Vérifier si le patient a été consulté avant d'etre hospitalisé
    if patient.consultation_set.exists():
        if request.method == 'POST':
            form = HospitalisationForm(request.POST)
            if form.is_valid():
                hospitalisation = form.save(commit=False)
                hospitalisation.patient = patient
                hospitalisation.save()
                return redirect('liste_patients')
        else:
            form = HospitalisationForm()
        return render(request, 'hospitaliser_patients.html', {'patient': patient, 'form': form})
    else:
        messages.error(request, "Le patient doit être consulté avant d'être hospitalisé.")
    return redirect('liste_patients')


#Cette vue nous permet d'afficher les patients hospitalisés
@login_required(login_url='urllogin')
def patients_hospitalises(request):
    patients_hospitalises = Hospitalisation.objects.all()
    return render(request, 'liste_patient_hospitalise.html', {'patients_hospitalises': patients_hospitalises})


#vue permettant d'inserer un nouveau patient
@login_required(login_url='urllogin')
def ajouter_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_patients')  # Rediriger vers la page de liste des patients après l'ajout
    else:
        form = PatientForm()
    return render(request, 'ajouter_patients.html', {'form': form})






#vue pour afficher le statut du patient si il est consulté ou pas , hospitalisé ou pas
@login_required(login_url='urllogin')
def statut_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'statut_patients.html', {'patient': patient})


@login_required(login_url='urllogin')
def modifier_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('liste_patients')  # Rediriger vers la liste des patients après modification
    else:
        form = PatientForm(instance=patient)
    return render(request, 'modifier_patient.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    return redirect('liste_patients')  # Redirection vers la liste des patients après suppression







@login_required(login_url='urllogin')
def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'liste_salle.html', {'salles': salles})


@login_required(login_url='urllogin')
def ajouter_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_salles')
    else:
        form = SalleForm()
    return render(request, 'ajouter_salle.html', {'form': form})


@login_required(login_url='urllogin')
def modifier_salles(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)
    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            return redirect('liste_salles')  # Rediriger vers la liste des salles après modification
    else:
        form = SalleForm(instance=salle)
    return render(request, 'modifier_salle.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_salles(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)
    salle.delete()
    return redirect('liste_salles')  # Redirection vers la liste des salles après suppression








@login_required(login_url='urllogin')
def liste_examens(request):
    examens = Examen.objects.all()
    return render(request, 'liste_examens.html', {'examens': examens})


@login_required(login_url='urllogin')
def ajouter_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_examens')
    else:
        form = ExamenForm()
    return render(request, 'ajouter_examen.html', {'form': form})


@login_required(login_url='urllogin')
def modifier_examen(request, examen_id):
    examen = get_object_or_404(Examen, pk=examen_id)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            return redirect('liste_examens')  # Rediriger vers la liste des salles après modification
    else:
        form = ExamenForm(instance=examen)
    return render(request, 'modifier_examen.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_examen(request, examen_id):
    examen = get_object_or_404(Examen, pk=examen_id)
    examen.delete()
    return redirect('liste_examens')  # Redirection vers la liste des examens après suppression








@login_required(login_url='urllogin')
def liste_laboratoires(request):
    laboratoires = Laboratoire.objects.all()
    return render(request, 'liste_laboratoires.html', {'laboratoires': laboratoires})


@login_required(login_url='urllogin')
def ajouter_laboratoire(request):
    if request.method == 'POST':
        form = LaboratoireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_laboratoires')
    else:
        form = LaboratoireForm()
    return render(request, 'ajouter_laboratoire.html', {'form': form})


@login_required(login_url='urllogin')
def modifier_laboratoire(request, laboratoire_id):
    laboratoire = get_object_or_404(Laboratoire, pk=laboratoire_id)
    if request.method == 'POST':
        form = LaboratoireForm(request.POST, instance=laboratoire)
        if form.is_valid():
            form.save()
            return redirect('liste_laboratoires')
    else:
        form = LaboratoireForm(instance=laboratoire)
    return render(request, 'modifier_laboratoire.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_laboratoire(request, laboratoire_id):
    laboratoire = get_object_or_404(Laboratoire, pk=laboratoire_id)
    laboratoire.delete()
    return redirect('liste_laboratoires')  # Redirection vers la liste des laboratoires après suppression









@login_required(login_url='urllogin')
def liste_services(request):
    services = Service.objects.all()
    return render(request, 'liste_services.html', {'services': services})


@login_required(login_url='urllogin')
def ajouter_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_services')
    else:
        form = ServiceForm()
    return render(request, 'ajouter_service.html', {'form': form})


@login_required(login_url='urllogin')
def modifier_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('liste_services')  # Rediriger vers la liste des services après modification
    else:
        form = ServiceForm(instance=service)
    return render(request, 'modifier_service.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    service.delete()
    return redirect('liste_services')  # Redirection vers la liste des services après suppression








@login_required(login_url='urllogin')
def liste_medecins(request):
    medecins = Medecin.objects.all()
    return render(request, 'liste_medecins.html', {'medecins': medecins})


@login_required(login_url='urllogin')
def ajouter_medecin(request):
    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medecins')
    else:
        form = MedecinForm()
    return render(request, 'ajouter_medecin.html', {'form': form})


@login_required(login_url='urllogin')
def modifier_medecin(request, medecin_id):
    medecin = get_object_or_404(Medecin, pk=medecin_id)
    if request.method == 'POST':
        form = MedecinForm(request.POST, instance=medecin)
        if form.is_valid():
            form.save()
            return redirect('liste_medecins')  # Rediriger vers la liste des médecins après modification
    else:
        form = MedecinForm(instance=medecin)
    return render(request, 'modifier_medecin.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_medecin(request, medecin_id):
    medecin = get_object_or_404(Medecin, pk=medecin_id)
    medecin.delete()
    return redirect('liste_medecins')  # Redirection vers la liste des médecins après suppression











@login_required(login_url='urllogin')
def liste_patients_examines(request):
    patients_examines = PatientExamine.objects.all()
    return render(request, 'liste_patients_examines.html', {'patients_examines': patients_examines})


@login_required(login_url='urllogin')
def ajouter_patient_examine(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        form = PatientExamineForm(request.POST)
        if form.is_valid():
            patient_examine = form.save(commit=False)
            patient_examine.patient = patient
            patient_examine.save()
            return redirect('liste_patients')  # Rediriger vers la liste des patients après l'ajout
    else:
        form = PatientExamineForm()
    return render(request, 'ajouter_patient_examine.html', {'form': form, 'patient': patient})

@login_required(login_url='urllogin')
def modifier_patient_examine(request, patient_examine_id):
    patient_examine = get_object_or_404(PatientExamine, pk=patient_examine_id)
    if request.method == 'POST':
        form = PatientExamineForm(request.POST, instance=patient_examine)
        if form.is_valid():
            form.save()
            return redirect('liste_patients_examines', patient_examine_id=patient_examine_id)
    else:
        form = PatientExamineForm(instance=patient_examine)
    return render(request, 'modifier_patient_examine.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_patient_examine(request, patient_examine_id):
    patient_examine = get_object_or_404(PatientExamine, pk=patient_examine_id)
    patient_examine.delete()
    messages.success(request, "Le patient examiné a été supprimé avec succès.")
    return redirect('liste_patients_examines')  # Redirection vers la liste des patients examinés après suppression






@login_required(login_url='urllogin')
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})


@login_required(login_url='urllogin')
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  # Rediriger vers la liste des produits après l'insertion
    else:
        form = ProduitForm()
    return render(request, 'ajouter_produit.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    produit.delete()
    return redirect('liste_produits')  # Rediriger vers la liste des produits après suppression


@login_required(login_url='urllogin')
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  # Rediriger vers la liste des produits après modification
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'modifier_produit.html', {'form': form})








@login_required(login_url='urllogin')
def liste_ventes(request):
    ventes = Vente.objects.all()
    for vente in ventes:
        vente.total = ExpressionWrapper(F('quantite_vendue') * F('produit__prix_unitaire'), output_field=DecimalField())
    return render(request, 'liste_ventes.html', {'ventes': ventes})


@login_required(login_url='urllogin')
def vendre_produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            quantite_vendue = form.cleaned_data['quantite_vendue']
            if quantite_vendue <= produit.quantite_stock:
                produit.quantite_stock -= quantite_vendue
                produit.save()
                # Enregistrez la vente ou effectuez d'autres opérations nécessaires
                return redirect('liste_produits')  # Rediriger vers la liste des produits après la vente
            else:
                # Gérer le cas où la quantité demandée est supérieure à celle en stock
                # Vous pouvez afficher un message d'erreur ou rediriger vers une autre page
                pass
    else:
        form = VenteForm()
    return render(request, 'vendre_produit.html', {'form': form, 'produit': produit})

@login_required(login_url='urllogin')
def modifier_vente(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('liste_ventes')  # Rediriger vers la liste des ventes après modification
    else:
        form = VenteForm(instance=vente)
    return render(request, 'modifier_vente.html', {'form': form})


@login_required(login_url='urllogin')
def supprimer_vente(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    vente.delete()
    return redirect('liste_ventes')  # Rediriger vers la liste des ventes après suppression


