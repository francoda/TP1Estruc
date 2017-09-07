import random

class Tablero():

    def __init__(self, filas, columnas):
        self.tablero = [["-"] * columnas for _ in range(filas)]

    def random(self, celulas_vivas):
        if(celulas_vivas > 0 and celulas_vivas < len(self.tablero)*len(self.tablero)):
            combinaciones = []
            for fila in range(len(self.tablero)):
                for columna in range(len(self.tablero)):
                    combinaciones.append((fila,columna))
            random.shuffle(combinaciones)
            while celulas_vivas > 0:
                combinacion_random = combinaciones.pop()
                self.tablero[combinacion_random[0]][combinacion_random[1]] = '*'
                celulas_vivas -= 1
        else:
            raise IndexError

    def set_value(self, fila, columna, valor):
        if fila > 0 and columna > 0 and fila < len(self.tablero[0]) and fila < len(self.tablero):
            raise IndexError
        elif valor != "-" or valor != "*":
            raise Exception("Valor incorrecto(Valores posibles:[-,*])")
        else:
            self.tablero[columna][fila] = valor

    def imprimir_tablero(self):
        for t in self.tablero:
            print(str(t))
