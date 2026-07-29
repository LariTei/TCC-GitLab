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
    valor_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Conserto
        fields = '__all__'