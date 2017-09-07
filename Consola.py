from enum import IntEnum
import os

class Menu():

    def __init__(self):
        while True:
            try:
                menu_principal = self.leer_entero('Menu Principal: \n'
                                                     '1 - Nuevo Juego \n'
                                                     '2 - Cargar Partida \n' 
                                                     '0 - Salir \n')
                if menu_principal == int(Menu_Principal.NUEVO_JUEGO):
                    print('Nuevo Juego')
                elif menu_principal == int(Menu_Principal.CARGAR_PARTIDA):
                    print('Cargar Partida')
                else: # SALIR
                    print('Salir')
                self.leer_entero('0 - Salir \n')
            except:
                print('Ocurrio un error en el programa. \n')
            self.limpiar()

    def leer_entero(self, texto):
        valor = ''
        while valor == '':
            try:
                valor = eval(input(texto))
                valores = [int(s) for s in texto.split() if s.isdigit()]
                if valor in valores:
                    return valor
            except:
                print('Por favor, ingrese un valor valido: {' + [int(s) for s in texto.split() if s.isdigit()] + '}')
            valor = ''

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Menu_Principal(IntEnum):
    SALIR = 0
    NUEVO_JUEGO = 1
    CARGAR_PARTIDA = 2


class Modo_De_Juego(IntEnum):
    SALIR = 0
    NORMAL = 1
    VIDA_ESTATICA = 2

class Modo_De_Generacion(IntEnum):
    SALIR = 0
    RANDOM = 1
    MANUAL = 2

class Accion(IntEnum):
    SALIR = 0
    SIGUENTE = 1
    MODIFICAR = 2

if __name__ == '__main__':
    Menu()