from django.db import models
from django.db import models

class Offre(models.Model):
    id = models.AutoField(primary_key=True)  # ID auto-incrément explicite
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)  # automatique à la création
    date_fin = models.DateField()

    def __str__(self):
        return self.titre

class Candidature(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    id_offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')

    def __str__(self):
        return f"{self.nom} - {self.id_offre.titre}"
