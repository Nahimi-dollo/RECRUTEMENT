from rest_framework import serializers
from .models import Offre
from .models import Candidature

class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['id', 'titre', 'description', 'date_publication', 'date_fin']
        read_only_fields = ['id', 'date_publication']
class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = '__all__'
        fields = ['id', 'nom','email','cv', 'id_offre']
        read_only_fields = ['id', 'cv']