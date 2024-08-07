from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Salle(models.Model):
    nom = models.CharField(max_length=50)
    capacite = 5
    
    def __str__(self):
        return self.nom
    


class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    ce_que_vous_ressenter = models.TextField()
    mail = models.EmailField()
    portable = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    montant_pour_consultation = models.PositiveIntegerField(default=0)
    date_de_consultation = models.DateTimeField(auto_now_add=True)
    avis_du_medecin = models.TextField()
    
    def __str__(self):
        return f"Consultation de {self.patient}"


class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, related_name='patients', on_delete=models.CASCADE)
    date_entree_hospitalise = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hospitalisation de {self.patient}"

@receiver(pre_save, sender=Hospitalisation)
def verifier_consultation(sender, instance, **kwargs):
    # Vérifier si le patient a été consulté avant d'être hospitalisé
    consultation_existante = Consultation.objects.filter(patient=instance.patient).exists()
    if not consultation_existante:
        raise ValidationError("Le patient doit être consulté avant d'être hospitalisé.")


@receiver(pre_save, sender=Hospitalisation)
def verifier_capacite_salle(sender, instance, **kwargs):
    #Verifie si la capacité maximale de la salle n'a pas atteint sa limite
    salle = instance.salle
    #Si le nombre de patients dans la salle est supérieur ou égale à 5 qui est est la capacité maximale de la salle on renvoie un message d'erreur
    if salle.patients.count() >= salle.capacite:
        raise ValidationError("La salle est pleine, impossible d'ajouter un nouveau patient.")



class Examen(models.Model):
    nom = models.CharField(max_length=100)
    desciption = models.TextField()
    
    def __str__(self):
        return self.nom
    

class Laboratoire(models.Model):
    nom_laboratoire = models.CharField(max_length=100)
    desciption_labo = models.TextField()

    def __str__(self):
        return self.nom_laboratoire
    

class Service(models.Model):
    nom_service = models.CharField(max_length=100)
    labo_requis = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_service
    

class Medecin(models.Model):
    nom_medecin = models.CharField(max_length=100)
    prenom_medecin = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Medecin {self.nom_medecin} - {self.prenom_medecin}"
    


class PatientExamine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    nom_du_labo = models.ForeignKey(Laboratoire, on_delete=models.CASCADE)
    date_examen = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} - {self.examen}"
    

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nom
    


class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_vendue = models.PositiveIntegerField()
    date_vente = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Vente de {self.quantite_vendue} {self.produit.nom} le {self.date_vente}"
    
    def clean(self):
        if self.quantite_vendue > self.produit.quantite_stock:
            raise ValidationError("La quantité en stock est insuffisante pour effectuer cette vente.")

    def save(self, *args, **kwargs):
        self.produit.quantite_stock -= self.quantite_vendue
        self.produit.save()
        super().save(*args, **kwargs)