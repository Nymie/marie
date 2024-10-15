from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Médecin'),
        ('ong', 'ONG'),
        ('donateur', 'Donateur'),
        ('admin', 'Administrateur'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='donateur')

    def __str__(self):
        return self.username

class Enfant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50, blank=True, null=True)  # Ajout du champ prénom
    age = models.IntegerField()
    groupe_sanguin = models.CharField(max_length=3, blank=True, null=True)  # Ajout du champ groupe sanguin
    statut = models.CharField(max_length=50, blank=True, null=True)  # Ajout du champ statut
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # Lien avec le modèle Utilisateur

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom else self.nom


