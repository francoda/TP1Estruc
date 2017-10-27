import random
import os
from enum import Enum, IntEnum
from Material.combination import combinations
from Excepciones import *

class Tablero():

    def __init__(self, filas, columnas):
        self.tablero = [[Celula.MUERTA] * columnas for _ in range(filas)]
        self.logTableros = []
        self.modo_de_juego = Modo_De_Juego.NOTSET
        self.modo_de_generacion = Modo_De_Generacion.NOTSET
        self.celulas_random = 0
        self.finalizo = False
        self.estatico = False

    def __eq__(self, other):
        if isinstance(other, Tablero):
            for x in range(len(self.tablero)):
                for y in range(len(self.tablero[0])):
                    if self.tablero[x][y] != other.tablero[x][y]:
                        return False
            return True
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def random(self, celulas_vivas):
        self.celulas_random = celulas_vivas
        if(celulas_vivas > 0 and celulas_vivas < len(self.tablero)*len(self.tablero[0])):
            combinaciones = []
            for fila in range(len(self.tablero)):
                for columna in range(len(self.tablero[0])):
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
            raise FormatoIncorrecto('Valor incorrecto(Valores posibles:[ ' + str(Celula.MUERTA) + ' , ' + str(Celula.VIVA) + '])')
        elif valor == '':
            self.tablero[fila][columna] = Celula.VIVA if self.tablero[fila][columna] == Celula.MUERTA else Celula.MUERTA
        else:
            self.tablero[fila][columna] = valor

    def calcular_adjacentes_vivos(self, fila, columna):
        celdas_vivas_alrededor = 0
        for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if (fila + x >= 0 and fila + x < len(self.tablero) and (columna + y >= 0 and columna + y < len(
                    self.tablero[0]))):  # Verifica que este dentro del tablero
                if (self.tablero[fila + x][columna + y] == Celula.VIVA):
                    celdas_vivas_alrededor += 1
        return celdas_vivas_alrededor

    def actualizar_celulas(self):
        new_gen = Tablero(len(self.tablero), len(self.tablero[0]))
        contador_vivas = 0
        for x in range(len(self.tablero)):
            for y in range(len(self.tablero[x])):
                adjacentes = self.calcular_adjacentes_vivos(x, y)
                if (self.tablero[x][y] == Celula.MUERTA):
                    if (adjacentes >= 3):
                        new_gen.tablero[x][y] = Celula.VIVA
                        contador_vivas +=1
                else:
                    if adjacentes == 2 or adjacentes == 3:
                        new_gen.tablero[x][y] = Celula.VIVA
                        contador_vivas += 1
        self.finalizo = self == new_gen or (len(self.logTableros) > 1 and self.logTableros[len(self.logTableros)-1] == new_gen) or contador_vivas == 0
        self.estatico = self.finalizo and contador_vivas != 0
        self.logTableros.append(new_gen)
        self.tablero = new_gen.tablero

    def vida_estatica(self):
        tableros_estaticos = []
        if (self.celulas_random <= (len(self.tablero) * len(self.tablero[0]))):
            for x in combinations(range(len(self.tablero) * len(self.tablero[0])), self.celulas_random):
                self.logTableros.clear()
                self.finalizo = False
                self.estatico = False
                self.tablero = Tablero(len(self.tablero), len(self.tablero[0])).tablero
                for posicion_tupla in x:
                    self.set_value(posicion_tupla // len(self.tablero), posicion_tupla % len(self.tablero[0]), Celula.VIVA)
                contador = 0
                while not self.estatico:
                    self.actualizar_celulas()
                    contador += 1
                    if contador > 30:
                        break

                if self.estatico:
                    self.limpiar()
                    conbinacion = "Combinación: " + str(x)
                    print(conbinacion)
                    print("Tablero estático encontrado: ")
                    impresion = self.impresion_tablero()
                    print(impresion)
                    tableros_estaticos.append(conbinacion + '\n' + impresion)
        else:
            raise IndexError
        self.limpiar()
        print("Tableros estáticos encontrados: ")
        for t in tableros_estaticos:
            print(t)

    def impresion_tablero(self):
        return '\n'.join([''.join(['{:2}'.format(Celula.value) for Celula in row]) for row in self.tablero])

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Celula(Enum):
    MUERTA = '-'
    VIVA = '*'

class Modo_De_Juego(IntEnum):
    NOTSET = 0
    NORMAL = 1
    PASOAPASO = 2
    VIDA_ESTATICA = 3

class Modo_De_Generacion(IntEnum):
    NOTSET = 0
    RANDOM = 1
    MANUAL = 2