# src/serializers.py
from rest_framework import serializers
from .models import Motorista, Automovel, Conserto

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = '__all__'

class AutomovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automovel
        fields = '__all__'

class ConsertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conserto
        fields = '__all__'