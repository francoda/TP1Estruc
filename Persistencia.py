import shelve
import os

class persistencia(object):

    @staticmethod
    def printList():
        partidas = shelve.open('Partidas')
        for nombre, tablero in partidas.items():
            print(nombre)
            print(tablero.impresion_tablero())
        partidas.close()

    @staticmethod
    def guardar(tablero_celular, nombre):
        partidas = shelve.open('Partidas')
        partidas[nombre] = tablero_celular
        partidas.close()
        input('Tablero guardado con éxito.\nPresione la tecla "Enter" para continuar...')

    @staticmethod
    def cargar(nombre):
        partidas = shelve.open('Partidas')

        if nombre in partidas:
            tablero_celular = partidas[nombre]
            print('Tablero cargado con éxito.\nPresione la tecla "Enter" para continuar...')
            return tablero_celular
        else:
            raise IOError('El nombre ingresado no corresponde a una partida previamente guardada')

