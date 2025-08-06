
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OffreSerializers
from .serializers import CandidatureSerializers
from .models import Offre
from .models import Candidature
from django.shortcuts import render, get_object_or_404, redirect



#--------------------------------- PARTIE CRUD OFFRE D'EMPLOI------------------------------------------#

@api_view(['POST'])
def AjoutOffre (request):
    serializer = OffreSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
def modifier_offres(request, id):
    try:
        offre = Offre.objects.get(id=id)
    except Offre.DoesNotExist:
        return Response({"error": "Offre non trouvée."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OffreSerializers (instance=offre, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT'])
def modifier_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == 'GET':
        serializer = OffreSerializers(offre)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OffreSerializers(offre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def supprimer_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    offre.delete()
    return Response({'message': f'Offre avec id {offre_id} supprimée avec succès.'}, status=status.HTTP_204_NO_CONTENT)

#--------------------------------- FIN CRUD OFFRE D'EMPLOI------------------------------------------#

#--------------------------------- PARTIE CRUD CANDIDATURE------------------------------------------#

@api_view(['POST'])
def AjoutCAndidature (request):
    serializer = CandidatureSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def modifier_candidature(request, id):
    try:
        candidature = Candidature.objects.get(id=id)
    except Candidature.DoesNotExist:
        return Response({"error": "Candidature non trouvée."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CandidatureSerializers (instance=candidature, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def supprimer_candidature(request, id):
    try:
        candidature = Candidature.objects.get(id=id)
    except Candidature.DoesNotExist:
        return Response({"error": "Candidature non trouvée."}, status=status.HTTP_404_NOT_FOUND)

    candidature.delete()
    return Response({"message": "Candidature supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)

#--------------------------------- FIN CRUD CANDIDATURE------------------------------------------#
