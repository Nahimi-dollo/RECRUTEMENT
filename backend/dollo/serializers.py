from rest_framework import serializers
from .models import Offre
from .models import Candidature

class OffreSerializers(serializers.ModelSerializer):
    class Meta : 
        model =Offre
        fields=['id','titre','description','date_publication', 'date_fin']
        read_only_fields = ['id','date_publication']


class CandidatureSerializers(serializers.ModelSerializer):
    class Meta :
        model = Candidature
        fields=['id', 'nom','email', 'cv', 'date_depot', 'telephone']  
        read_only_fields =  ['id', 'date_depot']   