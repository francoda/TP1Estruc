import shelve
import os

class persistencia(object):

    @staticmethod
    def printList():
        partidas = shelve.open('Partidas')
        for nombre, tablero in partidas.items():
            print(nombre)
            tablero.imprimir_tablero()
        partidas.close()

    @staticmethod
    def guardar(tablero_celular, nombre):
        partidas = shelve.open('Partidas')
        partidas[nombre] = tablero_celular
        partidas.close()
        print("Tablero guardado con éxito.")

    @staticmethod
    def cargar(nombre):
        partidas = shelve.open('Partidas')

        if nombre in partidas:
            tablero_celular = partidas[nombre]
            print("Tablero cargado con éxito.")
            return tablero_celular
        else:
            raise Exception('El nombre ingresado no corresponde a una partida previamente guardada')

