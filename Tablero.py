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
        fila -= 1
        columna -= 1
        if fila < 0 and columna < 0 and fila > len(self.tablero[0]) and fila > len(self.tablero):
            raise IndexError
        elif valor != '' and valor != Celula.MUERTA and valor != Celula.VIVA:
            raise Exception('Valor incorrecto(Valores posibles:[ ' + str(Celula.MUERTA) + ' , ' + str(Celula.VIVA) + '])')
        elif valor == '':
            self.tablero[columna][fila] = Celula.VIVA if self.tablero[columna][fila] == Celula.MUERTA else Celula.MUERTA
        else:
            self.tablero[columna][fila] = valor

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
        self.tablero = new_gen.tablero

    def imprimir_tablero(self):
        print('\n'.join([''.join(['{:4}'.format(Celula.value) for Celula in row]) for row in self.tablero]))

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