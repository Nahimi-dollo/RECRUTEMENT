from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .models import Offre, Candidature, Evaluation, Resultat
from .serializers import OffreSerializer, CandidatureSerializer, EvaluationSerializer, ResultatSerializer

from django.views.decorators.clickjacking import xframe_options_exempt




# ==================== OFFRES ====================
@api_view(['POST'])
def ajout_offre(request):
    serializer = OffreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def liste_offres(request):
    offres = Offre.objects.all()
    serializer = OffreSerializer(offres, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
def modifier_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    if request.method == 'GET':
        serializer = OffreSerializer(offre)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OffreSerializer(offre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    offre.delete()
    return Response({'message': f'Offre {offre_id} supprimée.'}, status=status.HTTP_204_NO_CONTENT)


# ==================== CANDIDATURES ====================
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def ajout_candidature(request):
    serializer = CandidatureSerializer(data=request.data)
    if serializer.is_valid():
        candidature = serializer.save()
        # Mail confirmation
        send_mail(
            subject="Confirmation de votre candidature",
            message=f"Bonjour {candidature.nom},\nVotre candidature a été enregistrée.",
            from_email=None,
            recipient_list=[candidature.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.static import serve
from django.views.decorators.clickjacking import xframe_options_exempt


@api_view(['GET'])
@xframe_options_exempt
def liste_candidatures(request):
    candidatures = Candidature.objects.all()
    serializer = CandidatureSerializer(candidatures, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@parser_classes([MultiPartParser, FormParser])
def modifier_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    if request.method == 'GET':
        serializer = CandidatureSerializer(candidature)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CandidatureSerializer(candidature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    candidature.delete()
    return Response({'message': f'Candidature {candidature_id} supprimée.'}, status=status.HTTP_204_NO_CONTENT)


# ==================== EVALUATIONS ====================
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evaluation
from .serializers import EvaluationSerializer

@api_view(['POST'])
def ajout_evaluation(request):
    serializer = EvaluationSerializer(data=request.data)
    
    if serializer.is_valid():
        # Sauvegarde de l'évaluation en respectant le serializer
        evaluation = serializer.save()

        # Retourner uniquement l'évaluation ajoutée
        return Response(
            {'message': 'Évaluation ajoutée ✅', 'evaluation': serializer.data},
            status=status.HTTP_201_CREATED
        )
    
    # Si données invalides
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def liste_evaluations(request):
    evaluations = Evaluation.objects.all()
    serializer = EvaluationSerializer(evaluations, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def modifier_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    serializer = EvaluationSerializer(evaluation, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    evaluation.delete()
    return Response({"message": f"Évaluation {evaluation_id} supprimée."}, status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Evaluation, Candidature
import urllib.parse

@api_view(['POST'])
def send_evaluation_email_to_all(request, evaluation_id):
    """
    Envoie un email à tous les candidats associés à l'offre d'une évaluation donnée
    avec un lien Jitsi généré automatiquement.
    """
    try:
        # Récupérer l'évaluation
        evaluation = Evaluation.objects.get(id=evaluation_id)
        if not evaluation.offre:
            return Response({"error": "Cette évaluation n'est associée à aucune offre."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les candidatures liées à l'offre de l'évaluation
        candidats = Candidature.objects.filter(offre=evaluation.offre)

        if not candidats.exists():
            return Response({"message": "Aucun candidat trouvé pour cette offre."},
                            status=status.HTTP_200_OK)

        # Générer un lien Jitsi unique pour cette évaluation
        # Exemple: https://meet.jit.si/Evaluation-<evaluation_id>-<offre_id>
        room_name = f"Evaluation-{evaluation.id}-Offre-{evaluation.offre.id}"
        # Encodage URL pour éviter les caractères invalides
        room_name_encoded = urllib.parse.quote(room_name)
        jitsi_link = f"https://meet.jit.si/{room_name_encoded}"

        # Envoyer le mail à chaque candidat
        for candidat in candidats:
            if not candidat.email:
                continue

            subject = "Invitation à votre évaluation en visioconférence"
            message = f"""
Bonjour {candidat.nom} {candidat.prenom},

Vous êtes invité(e) à participer à votre évaluation en visioconférence.

Date: {evaluation.date_evaluation.strftime('%d/%m/%Y') if evaluation.date_evaluation else 'non précisée'}
Heure: {evaluation.date_evaluation.strftime('%H:%M') if evaluation.date_evaluation else 'non précisée'}
Lien pour rejoindre la réunion: {jitsi_link}

Merci de votre ponctualité.
"""
            send_mail(
                subject,
                message,
                'no-reply@votreentreprise.com',
                [candidat.email],
                fail_silently=False
            )

        return Response({"message": f"Emails envoyés à {candidats.count()} candidat(s) avec le lien Jitsi."},
                        status=status.HTTP_200_OK)

    except Evaluation.DoesNotExist:
        return Response({"error": "Évaluation non trouvée."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==================== RESULTATS ====================
@api_view(['GET'])
def liste_resultats(request):
    resultats = Resultat.objects.all()
    serializer = ResultatSerializer(resultats, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def ajout_resultat(request):
    serializer = ResultatSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def modifier_resultat(request, resultat_id):
    resultat = get_object_or_404(Resultat, id=resultat_id)
    serializer = ResultatSerializer(resultat, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_resultat(request, resultat_id):
    resultat = get_object_or_404(Resultat, id=resultat_id)
    resultat.delete()
    return Response({'message': f'Résultat {resultat_id} supprimé.'}, status=status.HTTP_204_NO_CONTENT)

# ==================== VISIOCONFERENCE====================


import random
import string

def generate_jitsi_link(evaluation_id):
    # On crée un petit code unique pour éviter les doublons
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"https://meet.jit.si/Eval_{evaluation_id}_{suffix}"




