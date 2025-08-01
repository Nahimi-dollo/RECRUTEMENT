from django.shortcuts import render
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Offre
from django.core.mail import send_mail
from .serializers import OffreSerializer
from .serializers import CandidatureSerializer
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['GET'])
def bonjour(request):
    return Response({"message":"test toujours"})
@api_view(['GET'])
def test (request):
    return Response({"message":"test 2 pour "})

# ✅ Create
@api_view(['POST'])
def ajouter_offre(request):
    serializer = OffreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Read (All)
@api_view(['GET'])
def liste_offres(request):
    offres = Offre.objects.all()
    serializer = OffreSerializer(offres, many=True)
    return Response(serializer.data)

# ✅ Read (One)
@api_view(['GET'])
def detail_offre(request, pk):
    try:
        offre = Offre.objects.get(pk=pk)
    except Offre.DoesNotExist:
        return Response({"error": "Offre non trouvée"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OffreSerializer(offre)
    return Response(serializer.data)

# ✅ Update
@api_view(['PUT'])
def modifier_offre(request, pk):
    try:
        offre = Offre.objects.get(pk=pk)
    except Offre.DoesNotExist:
        return Response({"error": "Offre non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OffreSerializer(offre, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete
@api_view(['DELETE'])
def supprimer_offre(request, pk):
    try:
        offre = Offre.objects.get(pk=pk)
    except Offre.DoesNotExist:
        return Response({"error": "Offre non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    offre.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # Important pour gérer les fichiers
def candidater(request):
    serializer = CandidatureSerializer(data=request.data)
    if serializer.is_valid():
        candidature = serializer.save()

        # Récupérer l'email et le nom depuis la candidature enregistrée
        email = candidature.email  
        nom = candidature.nom      

        # Envoi de l'e-mail
        try:
            send_mail(
                subject="Confirmation de réception de votre candidature",
                message=f"Bonjour {nom},\n\nVotre candidature a bien été reçue. "
                        "Vous serez informé de la suite par e-mail.\n\nCordialement,\nL'équipe RH.",
                from_email=None,  # Utilisera DEFAULT_FROM_EMAIL dans settings.py
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur d'envoi de mail : {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)