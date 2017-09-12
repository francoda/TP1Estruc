import shelve
import os

class persistencia(object):

    def __init__(self):
        pass

    @staticmethod
    def guardar(tablero_celular, nombre):
        modulo_guardado = shelve.open('Partidas')
        modulo_guardado[nombre] = tablero_celular
        modulo_guardado.close()
        print("Tablero guardado con éxito.")

    @staticmethod
    def cargar(nombre):
        modulo_a_cargar = shelve.open('Partidas')

        if nombre in modulo_a_cargar:
            tablero_celular = modulo_a_cargar[nombre]
            print("Tablero cargado con éxito.")
            return tablero_celular
        else:
            raise Exception('El nombre ingresado no corresponde a una partida previamente guardada')

