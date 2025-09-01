from rest_framework import serializers
from .models import Offre, Candidature, Evaluation, Resultat

# ----------------------------
# Serializer Offre
# ----------------------------
class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['id', 'titre', 'description', 'date_publication', 'date_fin']
        read_only_fields = ['id', 'date_publication']

# ----------------------------
# Serializer Candidature
# ----------------------------


class CandidatureSerializer(serializers.ModelSerializer):
    cv_url = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidature
        fields = [
            'id','nom','prenom','email','telephone','adresse','date_naissance',
            'cv','photo_profil','offre','cv_url','photo_url'
        ]

    def get_cv_url(self, obj):
        if obj.cv:
            return obj.cv.url  # URL complète pour accéder au fichier
        return None

    def get_photo_url(self, obj):
        if obj.photo_profil:
            return obj.photo_profil.url
        return None

# ----------------------------
# Serializer Evaluation
# ----------------------------
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'offre', 'titre', 'note', 'commentaire', 'evaluateur', 'date_evaluation']
        read_only_fields = ['id']  # date_evaluation n'est plus read_only


# ----------------------------
# Serializer Resultat
# ----------------------------
class ResultatSerializer(serializers.ModelSerializer):
    # Nom et prénom du candidat via la candidature
    candidature_nom = serializers.CharField(source="candidature.nom", read_only=True)
    candidature_prenom = serializers.CharField(source="candidature.prenom", read_only=True)

    # Titre de l'offre via la candidature
    offre_titre = serializers.CharField(source="candidature.offre.titre", read_only=True)

    # Note de l'évaluation (peut être null)
    evaluation_note = serializers.SerializerMethodField()

    class Meta:
        model = Resultat
        fields = [
            'id',
            'candidature',
            'candidature_nom',
            'candidature_prenom',
            'offre_titre',
            'evaluation',
            'evaluation_note',
            'score',
            'statut',
            'date_resultat'
        ]
        read_only_fields = ['id', 'date_resultat']

    def get_evaluation_note(self, obj):
        """Retourne la note de l'évaluation si elle existe, sinon None"""
        if obj.evaluation:
            return obj.evaluation.note
        return None
