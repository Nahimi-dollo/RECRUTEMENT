from django.db import models
from django.utils import timezone


# ----------------------------
# Table Offre
# ----------------------------
class Offre(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=191)  # Limite compatible MySQL utf8
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    date_fin = models.DateField()

    def __str__(self):
        return self.titre


# ----------------------------
# Table Candidature
# ----------------------------
class Candidature(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=191)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    cv = models.FileField(upload_to="cv/", blank=True, null=True)
    photo_profil = models.ImageField(upload_to="photos/", blank=True, null=True)
    offre = models.ForeignKey(
        Offre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidatures"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.offre.titre if self.offre else 'Sans offre'}"


# ----------------------------
# Table Évaluation
# ----------------------------



class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    offre = models.ForeignKey(
        Offre,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )
    titre = models.CharField(max_length=191, default="Évaluation générale")
    note = models.FloatField()
    commentaire = models.TextField(blank=True, null=True)
    evaluateur = models.CharField(max_length=100)  # nom du RH
    date_evaluation = models.DateTimeField(help_text="Date et heure de l'évaluation")
    lien_visio = models.URLField(blank=True, null=True, help_text="Lien de la vidéoconférence")

    def __str__(self):
        return f"{self.titre} - {self.note}/10 pour {self.offre.titre} par {self.evaluateur}"



# ----------------------------
# Table Résultat
# ----------------------------
class Resultat(models.Model):
    id = models.AutoField(primary_key=True)

    # L'offre concernée par le résultat
    offre = models.ForeignKey(
        Offre,
        on_delete=models.CASCADE,
        related_name="resultats"
    )

    # Le candidat lié à ce résultat (via la table Candidature)
    candidature = models.ForeignKey(
        Candidature,
        on_delete=models.CASCADE,
        related_name="resultats"
    )

    # L'évaluation associée (facultative)
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name="resultats",
        null=True,
        blank=True
    )

    # Score final obtenu
    score = models.FloatField()

    # Statut du résultat
    statut = models.CharField(
        max_length=50,
        choices=[
            ("admis", "Admis"),
            ("recalé", "Recalé"),
            ("en attente", "En attente"),
        ],
        default="en attente"
    )

    # Date de création du résultat
    date_resultat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Résultat de {self.candidature.nom} pour {self.offre.titre} - {self.score}"