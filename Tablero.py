import random
import os
from enum import Enum, IntEnum
from Material.combination import combinations

class Tablero():

    def __init__(self, filas, columnas):
        self.tablero = [[Celula.MUERTA] * columnas for _ in range(filas)]
        self.tablero_antiguo = None
        self.modo_de_juego = Modo_De_Juego.NOTSET
        self.modo_de_generacion = Modo_De_Generacion.NOTSET
        self.diccionario_de_celdas = {}
        self.celulas_random = 0
        self.contador_vidas_estaticas = 0

    def random(self, celulas_vivas):
        self.celulas_random = celulas_vivas
        if(celulas_vivas > 0 and celulas_vivas < len(self.tablero)*len(self.tablero[0])):
            combinaciones = []
            for fila in range(len(self.tablero)):
                for columna in range(len(self.tablero)):
                    combinaciones.append((fila,columna))
            random.shuffle(combinaciones)
            while celulas_vivas > 0:
                combinacion_random = combinaciones.pop()
                self.tablero[combinacion_random[0]][combinacion_random[1]] = Celula.VIVA
                celulas_vivas -= 1
        else:
            raise IndexError

    def set_value(self, fila, columna, valor=''):
        fila -= 1
        columna -= 1
        if fila < 0 and columna < 0 and fila > len(self.tablero[0]) and fila > len(self.tablero):
            raise IndexError
        elif valor != '' and valor != Celula.MUERTA and valor != Celula.VIVA:
            raise Exception('Valor incorrecto(Valores posibles:[ ' + str(Celula.MUERTA) + ' , ' + str(Celula.VIVA) + '])')
        elif valor == '':
            self.tablero[fila][columna] = Celula.VIVA if self.tablero[fila][columna] == Celula.MUERTA else Celula.MUERTA
        else:
            self.tablero[fila][columna] = valor

    def calcular_adjacentes_vivos(self, fila, columna):
        distancia_de_celdas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        celdas_vivas_alrededor = 0
        for x, y in distancia_de_celdas:
            if (fila + x >= 0 and fila + x < len(self.tablero) and (columna + y >= 0 and columna + y < len(
                    self.tablero[0]))):  # Verifica que este dentro del tablero
                if (self.tablero[fila + x][columna + y] == Celula.VIVA):
                    celdas_vivas_alrededor += 1
        return celdas_vivas_alrededor

    def actualizar_celulas(self):
        new_gen = Tablero(len(self.tablero), len(self.tablero[0]))
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[x])):
                adjacentes = self.calcular_adjacentes_vivos(x, y)
                if (self.tablero[x][y] == Celula.MUERTA):
                    if (adjacentes >= 3):
                        new_gen.tablero[x][y] = Celula.VIVA
                else:
                    if adjacentes == 2 or adjacentes == 3:
                        new_gen.tablero[x][y] = Celula.VIVA
        self.tablero_antiguo = self.tablero
        self.tablero = new_gen.tablero
        self.cantidad_vidas_estaticas()

    def cantidad_vidas_estaticas(self):
        son_iguales = True
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[0])):
                if self.tablero[x][y] != self.tablero_antiguo[x][y]:
                    son_iguales = False
        if son_iguales:
            self.contador_vidas_estaticas += 1
        else:
            self.contador_vidas_estaticas = 0

    def consultar_estaticas(self):
        if self.diccionario_de_celdas == {}:
            for x in range(len(self.tablero)):
                for y in range(len(self.tablero[x])):
                    self.diccionario_de_celdas[(x, y)] = 0

        self.actualizar_celulas()
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[0])):
                if self.tablero[x][y] == self.tablero_antiguo[x][y]:
                    self.diccionario_de_celdas[(x, y)] = self.diccionario_de_celdas[(x, y)] + 1
                elif self.tablero[x][y] != self.tablero_antiguo[x][y]:
                    self.diccionario_de_celdas[(x, y)] = 0

    def vida_estatica(self):
        tableros_estaticos = []
        if (self.celulas_random <= (len(self.tablero) * len(self.tablero[0]))):
            for x in combinations(range(len(self.tablero) * len(self.tablero[0])), self.celulas_random):
                self.tablero = Tablero(len(self.tablero), len(self.tablero[0])).tablero
                self.contador_vidas_estaticas = 0
                self.diccionario_de_celdas = {}
                encontro = True
                contador = 0
                for posicion_tupla in x:
                    coordenadas = (
                        posicion_tupla // len(self.tablero[0]),
                        posicion_tupla % len(self.tablero[0]))
                    self.set_value(coordenadas[0], coordenadas[1], Celula.VIVA)

                while self.contador_vidas_estaticas < 3:
                    self.consultar_estaticas()
                    contador += 1
                    if contador > 30:
                        encontro = False
                        break

                if (not encontro):
                    self.limpiar()
                    print("Combinación: " + str(x))
                    print("Tablero estático encontrado: ")
                    self.imprimir_tablero()
                    tableros_estaticos.append(self)
        else:
            raise IndexError
        self.limpiar()
        print("Tableros estáticos encontrados: ")
        for t in tableros_estaticos:
            t.imprimir_tablero()
            print("---------------------------")

    def imprimir_tablero(self):
        print('\n'.join([''.join(['{:3}'.format(Celula.value) for Celula in row]) for row in self.tablero]))

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Celula(Enum):
    MUERTA = '-'
    VIVA = '*'

class Modo_De_Juego(IntEnum):
    NOTSET = 0
    NORMAL = 1
    VIDA_ESTATICA = 2

class Modo_De_Generacion(IntEnum):
    NOTSET = 0
    RANDOM = 1
    MANUAL = 2