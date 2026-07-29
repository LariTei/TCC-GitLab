# src/api_views.py
from rest_framework import viewsets
from .models import Motorista, Automovel, Conserto
from .serializers import MotoristaSerializer, AutomovelSerializer, ConsertoSerializer

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer


class AutomovelViewSet(viewsets.ModelViewSet):
    queryset = Automovel.objects.all()
    serializer_class = AutomovelSerializer


class ConsertoViewSet(viewsets.ModelViewSet):
    queryset = Conserto.objects.all()
    serializer_class = ConsertoSerializer