from Tablero import *
from Persistencia import *
import os

class Menu():

    def __init__(self):
        while True:
            try:
                self.limpiar()
                self.menu_principal = self.leer_entero('Menú Principal: \n'
                                                         '1 - Nuevo Juego \n'
                                                         '2 - Cargar Partida \n' 
                                                         '0 - Salir \n', True)
                # Cargo Tablero y configuracion
                if self.menu_principal == Menu_Principal.NUEVO_JUEGO:
                    while True:
                        try:
                            fila, columna = [int(x) for x in self.leer_string(
                                'Ingrese el tamaño en formato "fila x columna":').split('x')]
                            if fila > 30 or columna > 60:
                                raise Exception('Las dimensiones del tablero no deben superar a 30x60.')
                            if fila < 3 or columna < 3:
                                raise Exception('Las dimensiones del tablero deben superar a 3x3.')
                            self.tablero = Tablero(fila, columna)
                            break
                        except Exception as e:
                            self.leer_string(str(e) + ' \n Presione la tecla "Enter" para continuar...')
                elif self.menu_principal == Menu_Principal.CARGAR_PARTIDA:
                    self.tablero = persistencia.cargar(self.leer_string('Ingrese el nombre de la partida:'))
                elif self.menu_principal == Menu_Principal.SALIR:
                    break #Cierro el programa
                self.limpiar()
                # Cargo Configuraciones si no estan seteadas
                if self.tablero.modo_de_juego == Modo_De_Juego.NOTSET:
                    self.tablero.modo_de_juego = (self.leer_entero('Seleccione el modo de juego: \n'
                                                                     '1 - Normal \n'
                                                                     '2 - Vida Estática \n' 
                                                                     '0 - Salir \n', True))
                if self.tablero.modo_de_juego == Modo_De_Juego.NORMAL and self.tablero.modo_de_generacion == Modo_De_Generacion.NOTSET:
                    self.tablero.modo_de_generacion = self.leer_entero('Seleccione el método de generación: \n'
                                                                         '1 - Aleatorio \n'
                                                                         '2 - Manual \n' 
                                                                         '0 - Salir \n', True)
                    if self.tablero.modo_de_generacion == Modo_De_Generacion.RANDOM:
                        self.tablero.random(self.leer_entero('Ingresar número de celulas vivas:'))
                    elif self.tablero.modo_de_generacion == Modo_De_Generacion.MANUAL:
                        self.editar_tablero()
                    elif self.tablero.modo_de_generacion == Modo_De_Generacion.NOTSET:
                        break
                elif self.tablero.modo_de_juego == Modo_De_Juego.VIDA_ESTATICA:
                    self.tablero.random(self.leer_entero('Ingresar número de celulas vivas:'))
                # Inicia el juego
                self.limpiar()
                self.tablero.imprimir_tablero()
                while True:
                    if self.tablero.modo_de_juego == Modo_De_Juego.NORMAL:
                        self.accion = self.leer_entero('1 - Siguiente Generación \n'
                                                        '2 - Editar \n'
                                                        '3 - Guardar \n'
                                                        '0 - Salir \n', True)
                        if self.accion == Accion.SIGUENTE:
                           self.limpiar()
                           self.tablero.actualizar_celulas()
                           self.tablero.imprimir_tablero()
                        elif self.accion == Accion.EDITAR:
                            self.editar_tablero()
                        elif self.accion == Accion.GUARDAR:
                            persistencia.guardar(self.tablero, self.leer_string('Ingrese el nombre de la partida:'))
                        elif self.accion == Accion.SALIR:
                            break
                    elif self.tablero.modo_de_juego == Modo_De_Juego.VIDA_ESTATICA:
                        self.tablero.vida_estatica()
                        self.leer_string('Presione la tecla "Enter" para continuar...')
                        break

            except KeyboardInterrupt:
                persistencia.guardar(self.tablero, self.leer_string('Ingrese el nombre de la partida:'))
            except Exception as e:
                self.leer_string(str(e) + ' \n Presione la tecla "Enter" para continuar...')

    def editar_tablero(self):
        while True:
            try:
                fila, columna = [int(x) for x in self.leer_string(
                    'Ingresar coordenadas de la célula que desea modificar en formato "fila x columna":').split('x')]
                self.limpiar()
                self.tablero.set_value(fila, columna)
                self.tablero.imprimir_tablero()
                if self.leer_entero('1 - Modificar otra célula \n'
                                    '0 - Iniciar Juego \n') == 0:
                    break
            except Exception as e:
                self.leer_string(str(e) + ' \n Presione la tecla "Enter" para continuar')
        self.limpiar()

    def leer_entero(self, texto, tomar_valores=False):
        valor = ''
        while valor == '':
            try:
                valor = int(input(texto))
                if tomar_valores:
                    valores = [int(s) for s in texto.split() if s.isdigit()]
                    if valor in valores:
                        return valor
                    else:
                        raise IndexError
                else:
                    return valor
            except:
                print('Por favor, ingrese un número correspondiente al menú:' + str([int(s) for s in texto.split() if s.isdigit()]))
            valor = ''

    def leer_string(self, texto):
        while True:
            try:
                return input(texto)
            except:
                pass

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

class Menu_Principal(IntEnum):
    SALIR = 0
    NUEVO_JUEGO = 1
    CARGAR_PARTIDA = 2

class Accion(IntEnum):
    SALIR = 0
    SIGUENTE = 1
    EDITAR = 2
    GUARDAR = 3

if __name__ == '__main__':
    Menu()
