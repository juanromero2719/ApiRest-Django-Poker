from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import JugadorSerializer, CartaSerializer
from .models import Jugador, Carta
import random
from . import mazo_poker
from .validacion_poker import validar_manos

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    def create(self, request, *args, **kwargs):

        data = request.data.copy()
        nombre = data.get('nombre', None)
        nombre = nombre.lower()
        data['nombre'] = nombre

        # Validar cantidad de jugadores

        if Jugador.objects.count() >= 4:
            return Response({"error": "La sala esta llena!"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Validar si existe un usuario con ese nombre
        
        if Jugador.objects.filter(nombre__iexact=nombre).exists():
            return Response({"error": "Ya existe un jugador con ese nombre!"},
                            status=status.HTTP_400_BAD_REQUEST)
      
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
               
            return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            error_message = {
                "error": "Datos inválidos proporcionados.",
                "detalles": serializer.errors
            }
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class CartaViewSet(viewsets.ViewSet):

    def entregar_cartas(self, request, jugador_id=None):

        # Busca al jugador
        try:
            jugador = Jugador.objects.get(pk=jugador_id)
        except Jugador.DoesNotExist:
            return Response({"error": "Jugador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Revisar cuantas cartas tiene el jugador
        cantidad_cartas = Carta.objects.filter(jugador=jugador).count()
        
        if(cantidad_cartas >= 5):
            return Response('El jugador ya ha solicitado cartas', status=status.HTTP_400_BAD_REQUEST)

        # Validar que no esten repetidas

        cartas_asignadas = Carta.objects.all()
        cartas_nuevas = []
        cartas_barajadas = random.sample(mazo_poker.cartas, 5)
        for carta_data in cartas_barajadas:

            # Validar que la carta no esté asignada a ningún jugador
            while cartas_asignadas.filter(numero=carta_data['numero'], tipo=carta_data['tipo'], color=carta_data['color']).exists():
                carta_data = random.choice(mazo_poker.cartas)

            carta = Carta.objects.create(jugador=jugador, **carta_data)
            serializer = CartaSerializer(carta)  # Serializar la carta
            cartas_nuevas.append(serializer.data)

        return Response({
            "cartas": cartas_nuevas
        }, status=status.HTTP_201_CREATED)
    
    def cambiar_cartas(self, request, jugador_id=None):
        # Buscar al jugador
        try:
            jugador = Jugador.objects.get(id=jugador_id)
        except Jugador.DoesNotExist:
            return Response({"error": "Jugador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Validar que el usuario tenga cambios
        if jugador.cambio >= 2:
            return Response('El jugador no tiene cambios disponibles', status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que el jugador tenga cartas
        try:
            cantidad_cartas = Carta.objects.filter(jugador=jugador).count()    
        except:
            return Response('El jugador no tiene cartas para cambiar', status=status.HTTP_400_BAD_REQUEST)
        
        cartas_cambiar = request.data.get('cartas', [])

        # Validar que el usuario envió cartas
        if len(cartas_cambiar) <= 0:
            return Response('Debes seleccionar una, dos o tres cartas para cambiar', status=status.HTTP_400_BAD_REQUEST)

        # Validar que se estén cambiando máximo 3 cartas
        if len(cartas_cambiar) > 3:
            return Response({"error": "Se pueden cambiar como máximo 3 cartas."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que las cartas existan y pertenezcan al jugador
        for carta_id in cartas_cambiar:
            try:
                carta = Carta.objects.get(pk=carta_id, jugador=jugador)
            except Carta.DoesNotExist:
                return Response({"error": f"La carta con id {carta_id} no existe o no pertenece al jugador."}, status=status.HTTP_404_NOT_FOUND)
        
        cartas_asignadas = Carta.objects.all()

        # Crear nuevas cartas que no estén asignadas a ningún jugador
        cartas_nuevas = []
        for _ in range(len(cartas_cambiar)):
            carta_data = random.choice(mazo_poker.cartas)
            while cartas_asignadas.filter(numero=carta_data['numero'], tipo=carta_data['tipo'], color=carta_data['color']).exists():
                carta_data = random.choice(mazo_poker.cartas)

            carta = Carta.objects.create(jugador=jugador, **carta_data)
            cartas_nuevas.append({
                "id": carta.id,
                "numero": carta_data['numero'],
                "tipo": carta_data['tipo'],
                "color": carta_data['color']
            })

        # Eliminar cartas cambiadas
        for carta_id in cartas_cambiar:
            carta = Carta.objects.get(pk=carta_id, jugador=jugador)
            carta.delete()

        # Agregar 1 cambio
        jugador.cambio += 1
        jugador.save()

        return Response({
            "mensaje": "Cartas cambiadas exitosamente.",
            "cartas_nuevas": cartas_nuevas
        }, status=status.HTTP_200_OK)
    
class PartidaViewSet(viewsets.ViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    def volverajugar(self, request):
        Carta.objects.all().delete()
        Jugador.objects.all().update(cambio=0)
        return Response({
            "mensaje": "Se han eliminado todas las cartas. ¡Volver a jugar!",
        }, status=status.HTTP_200_OK)

    def iniciarjuego(self, request):
        Jugador.objects.all().delete()
        Carta.objects.all().delete()

        return Response({
            "mensaje": "Se han eliminado todos los jugadores y cartas. ¡Juego iniciado!",
        }, status=status.HTTP_200_OK)

    def estado(self, request):
        jugadores = Jugador.objects.all()

        if len(jugadores) < 4:
            return Response('Deben haber mínimo 4 jugadores', status=status.HTTP_400_BAD_REQUEST)

        jugadores_con_manos_especiales = []
        jugadores_sin_cartas = []

        for jugador in jugadores:
            cartas = Carta.objects.filter(jugador=jugador)
            if cartas.exists():
                mano = validar_manos(cartas)
                if mano:
                    if not isinstance(mano, (list, tuple)):
                        mano = [mano]
                    jugadores_con_manos_especiales.append({"nombre": jugador.nombre, "manos": mano})
            else:
                jugadores_sin_cartas.append(jugador.nombre)

        if jugadores_sin_cartas:
            return Response({
                "mensaje": "No se puede iniciar la partida porque uno o más jugadores no tienen cartas asignadas.",
                "jugadores_sin_cartas": jugadores_sin_cartas
            }, status=status.HTTP_400_BAD_REQUEST)

        if not jugadores_con_manos_especiales:
            return Response({
                "mensaje": "No se encontraron jugadores con manos especiales."
            }, status=status.HTTP_200_OK)

        # Ordenar jugadores por la primera mano
        jugadores_con_manos_especiales.sort(key=lambda x: x['manos'][0], reverse=True)

        # Evaluar posibles empates en la primera mano
        ganadores = [jugadores_con_manos_especiales[0]]
        for jugador in jugadores_con_manos_especiales[1:]:
            if jugador["manos"][0] == ganadores[0]["manos"][0]:
                ganadores.append(jugador)
            else:
                break

        # Si hay más de un ganador, evaluar la segunda mano
        if len(ganadores) > 1:
            ganadores.sort(key=lambda x: x['manos'][1] if len(x['manos']) > 1 else 0, reverse=True)
            final_ganador = ganadores[0]
            if len(ganadores) > 1 and len(ganadores[0]["manos"]) > 1 and ganadores[0]["manos"][1] == ganadores[1]["manos"][1]:
                return Response({
                    #"jugadores": jugadores_con_manos_especiales,
                    "ganadores": ganadores
                }, status=status.HTTP_200_OK)
        else:
            final_ganador = ganadores[0]

        return Response({
            #"jugadores": jugadores_con_manos_especiales,
            "ganador": final_ganador
        }, status=status.HTTP_200_OK)