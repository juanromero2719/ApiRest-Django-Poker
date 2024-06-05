from django.test import TestCase
from .models import Carta, Jugador
from tabulate import tabulate
# Create your tests here.

# Ver jugadores + cambios

def ver_jugadores():

    jugadores = Jugador.objects.all()

    if len(jugadores) == 0:
        print("no hay jugadores")
  
    for jugador in jugadores:
        print(f"el jugador {jugador.nombre} tiene {jugador.cambio} cambios")

# Limpiar jugadores

def  limpiar_jugadores():
    Jugador.objects.all().delete()
    print("Se han limpiado todos los jugadores")

# Limpiar Cartas

def limpiar_cartas():
    Carta.objects.all().delete()
    print("se han limpiado todas las cartas")

# Cantidad de cartas por jugador - id

def cantidad_cartas_jugadores():
    jugadores = Jugador.objects.all().values('id')

    if len(jugadores) == 0:
        print("no hay jugadores")

    for jugador in jugadores:
        print(f"el jugador {jugador} tiene: {Carta.objects.filter(jugador=jugador['id']).count()}")

# Ver cartas de jugadores

def repetidas():
    # Obtener todos los jugadores
    jugadores = Jugador.objects.all()

    if len(jugadores) == 0:
        print("No hay jugadores")

    tabla_cartas = []

    # Recorrer cada jugador
    for jugador in jugadores:
        # Nombre del jugador
        nombre_jugador = jugador.nombre

        # Obtener todas las cartas del jugador
        cartas_jugador = Carta.objects.filter(jugador=jugador)

        # Lista de cartas del jugador en formato tabular
        cartas_tabular = []
        for carta in cartas_jugador:
            cartas_tabular.append([carta.id, carta.numero, carta.tipo, carta.color])

        # Agregar a la tabla general
        tabla_cartas.append({
            "Jugador": nombre_jugador,
            "Cartas": tabulate(cartas_tabular, headers=["ID", "Número", "Tipo", "Color"], tablefmt="grid")
        })

    # Mostrar la tabla por consola
    for item in tabla_cartas:
        print(f"Jugador: {item['Jugador']}")
        print(item['Cartas'])
        print("\n")

# Insertar mano

# Define las cartas para formar un doble par
cartas = [
{'numero': '2', 'tipo': 'corazones', 'color': 'rojo'},
    {'numero': '5', 'tipo': 'diamantes', 'color': 'rojo'},
    {'numero': '7', 'tipo': 'tréboles', 'color': 'negro'},
    {'numero': '9', 'tipo': 'picas', 'color': 'negro'},
    {'numero': 'K', 'tipo': 'corazones', 'color': 'rojo'}
]


def test_insertar_mano():
        # Limpiar las cartas existentes del jugador
        Carta.objects.filter(jugador=75).delete()
        
        jugador = Jugador.objects.get(id=75)

        # Insertar todas las cartas para el jugador
        for carta_data in cartas:
            Carta.objects.create(
                jugador= jugador,
                numero=carta_data['numero'],
                tipo=carta_data['tipo'],
                color=carta_data['color']
            )



#ver_jugadores()
#limpiar_jugadores()
#limpiar_cartas()
#cantidad_cartas_jugadores()
#test_insertar_mano()
repetidas()

#{ "cartas": [1, 3, 5] }
