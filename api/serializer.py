from rest_framework import serializers
from .models import Jugador, Carta

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = '__all__'

    def validar_nombre(self, value):

        if not value:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
            
        if Jugador.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("Ya existe un jugador con este nombre.")
            
        return value
    
class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = '__all__'