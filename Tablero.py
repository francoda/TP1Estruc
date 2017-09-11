import random
from enum import Enum, IntEnum

class Tablero():

    def __init__(self, filas, columnas):
        self.tablero = [[Celula.MUERTA] * columnas for _ in range(filas)]
        self.modo_de_juego = Modo_De_Juego.NOTSET
        self.modo_de_generacion = Modo_De_Generacion.NOTSET

    def random(self, celulas_vivas):
        if(celulas_vivas > 0 and celulas_vivas < len(self.tablero)*len(self.tablero)):
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
        if fila > 0 and columna > 0 and fila < len(self.tablero[0]) and fila < len(self.tablero):
            raise IndexError
        elif valor != '' or valor != Celula.MUERTA or valor != Celula.VIVA:
            raise Exception('Valor incorrecto(Valores posibles:[-,*])')
        elif valor == '':
            self.tablero[columna][fila] = Celula.VIDA if self.tablero[columna][fila] == Celula.MUERTA else Celula.VIDA
        else:
            self.tablero[columna][fila] = valor

    def calcular_adjacentes_vivos(self, fila, columna):
        distancia_de_celdas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        celdas_vivas_alrededor = 0
        for x, y in distancia_de_celdas:
            if (fila + x >= 0 and fila + x < len(self.matriz) and (columna + y >= 0 and columna + y < len(
                    self.matriz[0]))):  # Verifica que este dentro del tablero
                if (self.matriz[fila + x][columna + y] == '*'):
                    celdas_vivas_alrededor += 1
            return celdas_vivas_alrededor

    def actualizar_celulas(self):
        matriz_actualizada = self.matriz_nueva(len(self.matriz), len(self.matriz[0]))
        for x in range(len(self.matriz)):
            for y in range(len(self.matriz[x])):
                adjacentes = self.calcular_adjacentes_vivos(x, y)
                if (self.matriz[x][y] == '-'):
                    if (adjacentes >= 3):
                        matriz_actualizada[x][y] = '*'
                else:
                    if adjacentes == 2 or adjacentes == 3:
                        matriz_actualizada[x][y] = '*'
        self.matriz = matriz_actualizada

    def get_modo_de_juego(self):
        return self.modo_de_juego

    def set_modo_de_juego(self, modo_de_juego):
        self.modo_de_juego == modo_de_juego

    def get_modo_de_generacion(self):
        return self.modo_de_generacion

    def set_modo_de_generacion(self, modo_de_generacion):
        self.modo_de_generacion == modo_de_generacion

    def imprimir_tablero(self):
        for t in self.tablero:
            print(str(t))

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