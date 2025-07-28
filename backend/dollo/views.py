from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def bonjour(request):
    return Response({"message":"test toujours"})
@api_view(['GET'])
def test (request):
    return Response({"message":"test 2 pour "})


