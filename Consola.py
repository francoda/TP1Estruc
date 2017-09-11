from enum import IntEnum
from Tablero import *
import os

class Menu():

    def __init__(self):
        while True:
            try:
                self.menu_principal = self.leer_entero('Menu Principal: \n'
                                                         '1 - Nuevo Juego \n'
                                                         '2 - Cargar Partida \n' 
                                                         '0 - Salir \n', True)

                # Cargo Tablero y configuracion
                if self.menu_principal == Menu_Principal.NUEVO_JUEGO:
                    while True:
                        #try:
                            fila, columna = [int(x) for x in self.leer_string(
                                'Ingresar tamaño[{filas}x{columnas}]:').split('x')]
                            self.tablero = Tablero(fila, columna)
                            break
                        #except:
                        #   pass
                elif self.menu_principal == Menu_Principal.CARGAR_PARTIDA:
                    # TODO: Recuperar tablero
                    self.tablero #=
                elif self.menu_principal == Menu_Principal.SALIR:
                    break #Cierro el programa
                # Cargo Configuraciones si no estan seteadas
                if self.tablero.get_modo_de_juego == Modo_De_Juego.NOTSET:
                    self.tablero.set_modo_de_juego(self.leer_entero('Elegir modo de juego: \n'
                                                             '1 - Normal \n'
                                                             '2 - Vida Estética \n' 
                                                             '0 - Salir \n', True))
                if self.tablero.get_modo_de_juego != Modo_De_Juego.NOTSET and self.tablero.get_modo_de_generacion == Modo_De_Generacion.NOTSET:
                    self.tablero.set_modo_de_generacion(self.leer_entero('Elegir modo de generación: \n'
                                                                 '1 - Random \n'
                                                                 '2 - Manual \n' 
                                                                 '0 - Salir \n', True))
                    if self.tablero.get_modo_de_generacion == Modo_De_Generacion.RANDOM:
                        self.tablero.random(self.leer_entero('Ingresar numero de celulas vivas:'))
                    elif self.tablero.get_modo_de_generacion == Modo_De_Generacion.MANUAL:
                        while True:
                            try:
                                fila, columna = [int(x) for x in self.leer_string(
                                    'Ingresar coordenadas a cambiar[{fila}x{columna}]:').split('x')]
                                self.tablero.set_value(fila, columna)
                                self.tablero.imprimir_tablero()
                                break
                            except:
                                pass
            except Exception as e:
                input(str(e))


    def leer_entero(self, texto, tomar_valores=False):
        valor = ''
        while valor == '':
            try:
                self.limpiar()
                valor = eval(input(texto))
                if tomar_valores:
                    valores = [int(s) for s in texto.split() if s.isdigit()]
                    if valor in valores:
                        return valor
                else:
                    return valor
            except:
                print('Por favor, ingrese un valor valido: {' + [int(s) for s in texto.split() if s.isdigit()] + '}')
            valor = ''

    def leer_string(self, texto):
        while True:
            #try:
                self.limpiar()
                return input(texto)
            #except:
            #    pass

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Menu_Principal(IntEnum):
    SALIR = 0
    NUEVO_JUEGO = 1
    CARGAR_PARTIDA = 2

class Accion(IntEnum):
    SALIR = 0
    SIGUENTE = 1
    MODIFICAR = 2

if __name__ == '__main__':
    Menu()