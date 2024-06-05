from collections import Counter

def es_escalera_real(cartas):
    # Definición de la escalera real
    escalera_real = ["10", "J", "Q", "K", "A"]
    
    # Obtener los números y tipos de las cartas
    numeros = [carta.numero for carta in cartas]
    tipos = {carta.tipo for carta in cartas}
    
    # Función para obtener el valor numérico de la carta
    def valor_carta(carta):
        valores = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
            'Q': 12, 'K': 13, 'A': 14
        }
        return valores[carta]

    # Ordenar los números de las cartas
    numeros_ordenados = sorted(numeros, key=valor_carta)
    
    # Verificar si los números forman una escalera real y si todos los tipos son iguales
    return numeros_ordenados == escalera_real and len(tipos) == 1


def es_escalera_de_color(cartas):
    # Diccionario para asignar valores numéricos a las cartas
    valores_cartas = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
        'Q': 12, 'K': 13, 'A': 14
    }

    # Verificar que todas las cartas tengan el mismo tipo
    tipos = {carta.tipo for carta in cartas}
    if len(tipos) != 1:
        return False

    # Obtener los números de las cartas y convertirlos a valores numéricos
    numeros = []
    for carta in cartas:
        numero_carta = carta.numero
        if numero_carta in valores_cartas:
            numeros.append(valores_cartas[numero_carta])
        else:
            return False  # Si no es un número válido, no puede ser parte de una escalera

    # Ordenar los números en orden ascendente
    numeros_ordenados = sorted(numeros)

    # Verificar si los números forman una escalera
    for i in range(len(numeros_ordenados) - 1):
        if numeros_ordenados[i + 1] - numeros_ordenados[i] != 1:
            return False

    # Determinar el tipo de escalera de color
    min_index = min(numeros_ordenados)
    max_index = max(numeros_ordenados)

    if min_index == 2 and max_index == 6:
        return 8.02
    elif min_index == 3 and max_index == 7:
        return 8.03
    elif min_index == 4 and max_index == 8:
        return 8.04
    elif min_index == 5 and max_index == 9:
        return 8.05
    elif min_index == 6 and max_index == 10:
        return 8.06
    elif min_index == 7 and max_index == 11:
        return 8.07
    elif min_index == 8 and max_index == 12:
        return 8.08
    elif min_index == 9 and max_index == 13:
        return 8.09
    elif min_index == 10 and max_index == 14:
        return 8.10
    else:
        return False

def es_poker(cartas):
    numeros = [carta.numero for carta in cartas]
    cuenta_numeros = Counter(numeros)
    
    if 4 in cuenta_numeros.values():
        poker = next(key for key, value in cuenta_numeros.items() if value == 4)
        
        valor_poker = {
            'A': 7.14, 'K': 7.13, 'Q': 7.12, 'J': 7.11,
            '10': 7.10, '9': 7.09, '8': 7.08, '7': 7.07,
            '6': 7.06, '5': 7.05, '4': 7.04, '3': 7.03,
            '2': 7.02
        }.get(poker, 7.0)
        
        return valor_poker
    
    return False

def es_full(cartas):
    numeros = [carta.numero for carta in cartas]
    cuenta_numeros = Counter(numeros)
    
    if 3 in cuenta_numeros.values() and 2 in cuenta_numeros.values():
        trio = next(key for key, value in cuenta_numeros.items() if value == 3)
        par = next(key for key, value in cuenta_numeros.items() if value == 2)
        
        valor_trio = {
            'A': 6.14, 'K': 6.13, 'Q': 6.12, 'J': 6.11,
            '10': 6.10, '9': 6.09, '8': 6.08, '7': 6.07,
            '6': 6.06, '5': 6.05, '4': 6.04, '3': 6.03,
            '2': 6.02
        }.get(trio, 6.0)
        
        valor_par = {
            'A': 6.14, 'K': 6.13, 'Q': 6.12, 'J': 6.11,
            '10': 6.10, '9': 6.09, '8': 6.08, '7': 6.07,
            '6': 6.06, '5': 6.05, '4': 6.04, '3': 6.03,
            '2': 6.02
        }.get(par, 6.0)
        
        return valor_trio, valor_par
    
    return False

def valor_carta(carta):
    valores_cartas = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11,
        '10': 10, '9': 9, '8': 8, '7': 7,
        '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
    }
    return valores_cartas[carta]

def es_color(cartas):
    tipos = [carta.tipo for carta in cartas]
    return len(set(tipos)) == 1

def es_escalera(cartas):
    # Diccionario para asignar valores numéricos a las cartas
    valores_cartas = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
        'Q': 12, 'K': 13, 'A': 14
    }

    # Obtener los números de las cartas y convertirlos a valores numéricos
    numeros = []
    for carta in cartas:
        numero_carta = carta.numero
        if numero_carta in valores_cartas:
            numeros.append(valores_cartas[numero_carta])
        else:
            return False  # Si no es un número válido, no puede ser parte de una escalera

    # Ordenar los números en orden ascendente
    numeros_ordenados = sorted(numeros)

    # Verificar si los números forman una escalera
    for i in range(len(numeros_ordenados) - 1):
        if numeros_ordenados[i + 1] - numeros_ordenados[i] != 1:
            return False

    # Determinar el tipo de escalera
    min_index = min(numeros_ordenados)
    max_index = max(numeros_ordenados)

    if min_index == 2 and max_index == 6:
        return 4.02
    elif min_index == 3 and max_index == 7:
        return 4.03
    elif min_index == 4 and max_index == 8:
        return 4.04
    elif min_index == 5 and max_index == 9:
        return 4.05
    elif min_index == 6 and max_index == 10:
        return 4.06
    elif min_index == 7 and max_index == 11:
        return 4.07
    elif min_index == 8 and max_index == 12:
        return 4.08
    elif min_index == 9 and max_index == 13:
        return 4.08
    elif min_index == 10 and max_index == 14:
        return 4.10
    else:
        return False

def es_trio(cartas):
    numeros = [carta.numero for carta in cartas]
    cuenta_numeros = Counter(numeros)
    
    trio = [numero for numero, count in cuenta_numeros.items() if count == 3]
    
    if len(trio) == 1:
        trio_valor = trio[0]
        
        if trio_valor == 'A':
            return 3.14
        elif trio_valor == 'K':
            return 3.13
        elif trio_valor == 'Q':
            return 3.12
        elif trio_valor == 'J':
            return 3.11
        elif trio_valor == '10':
            return 3.10
        elif trio_valor == '9':
            return 3.09
        elif trio_valor == '8':
            return 3.08
        elif trio_valor == '7':
            return 3.07
        elif trio_valor == '6':
            return 3.06
        elif trio_valor == '5':
            return 3.05
        elif trio_valor == '4':
            return 3.04
        elif trio_valor == '3':
            return 3.03
        elif trio_valor == '2':
            return 3.02
        else:
            return 3.0
    
    return False

def es_doble_pareja(cartas):
    numeros = [carta.numero for carta in cartas]
    cuenta_numeros = Counter(numeros)
    
    pares = [numero for numero, count in cuenta_numeros.items() if count == 2]
    
    if len(pares) == 2:
        pareja1, pareja2 = pares
        
        valor_pareja1 = {
            'A': 2.14, 'K': 2.13, 'Q': 2.12, 'J': 2.11,
            '10': 2.10, '9': 2.09, '8': 2.08, '7': 2.07,
            '6': 2.06, '5': 2.05, '4': 2.04, '3': 2.03,
            '2': 2.02
        }.get(pareja1, 2.0)
        
        valor_pareja2 = {
            'A': 2.14, 'K': 2.13, 'Q': 2.12, 'J': 2.11,
            '10': 2.10, '9': 2.09, '8': 2.08, '7': 2.07,
            '6': 2.06, '5': 2.05, '4': 2.04, '3': 2.03,
            '2': 2.02
        }.get(pareja2, 2.0)
        
        return valor_pareja1, valor_pareja2
    
    return False

def es_pareja(cartas):
    numeros = [carta.numero for carta in cartas]
    cuenta_numeros = Counter(numeros)
    
    pareja = [numero for numero, count in cuenta_numeros.items() if count == 2]
    
    if len(pareja) == 1:
        pareja_valor = pareja[0]
        
        if pareja_valor == 'A':
            return 1.14
        elif pareja_valor == 'K':
            return 1.13
        elif pareja_valor == 'Q':
            return 1.12
        elif pareja_valor == 'J':
            return 1.11
        elif pareja_valor == '10':
            return 1.10
        elif pareja_valor == '9':
            return 1.09
        elif pareja_valor == '8':
            return 1.08
        elif pareja_valor == '7':
            return 1.07
        elif pareja_valor == '6':
            return 1.06
        elif pareja_valor == '5':
            return 1.05
        elif pareja_valor == '4':
            return 1.04
        elif pareja_valor == '3':
            return 1.03
        elif pareja_valor == '2':
            return 1.02
        else:
            return 1.0
    
    return False

def valor_carta_mas_alta(cartas):
    # Definición de los valores de las cartas
    valores = {
        '2': 0.02, '3': 0.03, '4': 0.04, '5': 0.05, '6': 0.06,
        '7': 0.07, '8': 0.08, '9': 0.09, '10': 0.10, 'J': 0.11,
        'Q': 0.12, 'K': 0.13, 'A': 0.14
    }

    # Ordenar los números de las cartas
    numeros = [carta.numero for carta in cartas]

    def valor_carta(carta):
        return valores[carta]

    numeros_ordenados = sorted(numeros, key=valor_carta)

    # Obtener la carta más alta y retornar su valor
    carta_mas_alta = numeros_ordenados[-1]
    return valores.get(carta_mas_alta, 0.0)

def validar_manos(cartas):
    if len(cartas) == 5:
        if es_escalera_real(cartas):
            return 9.1
        elif es_escalera_de_color(cartas):
            return es_escalera_de_color(cartas)
        elif es_poker(cartas):
            return es_poker(cartas)
        elif es_full(cartas):
            return es_full(cartas)
        elif es_color(cartas):
            return 5
        elif es_escalera(cartas):
            return es_escalera(cartas)
        elif es_trio(cartas):
            return es_trio(cartas)
        elif es_doble_pareja(cartas):
            return es_doble_pareja(cartas)
        elif es_pareja(cartas):
            return es_pareja(cartas)
        else:
            return valor_carta_mas_alta(cartas)
    return None