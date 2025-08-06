from django.db import models

class Offre(models.Model):
    id=models.AutoField(primary_key=True)
    titre=models.CharField(max_length=255)
    description=models.TextField()
    date_publication=models.DateField(auto_now_add=True)
    date_fin=models.DateField()
    def __str__(self):
        return self.titre()
    

class Candidature(models.Model):
    id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    date_depot=models.DateField(auto_now_add=True) 
    telephone=models.IntegerField(max_length=100)
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    def __str__(self):
        return self.nom() 
      

