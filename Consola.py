from Tablero import *
from Persistencia import *
from Excepciones import *
import os, time

class Menu():

    def __init__(self):
        while True:
            self.tablero = None
            self.limpiar()
            self.menu_principal = self.leer_entero('Menú Principal: \n'
                                                     '1 - Nuevo Juego \n'
                                                     '2 - Cargar Partida \n' 
                                                     '0 - Salir \n', True)
            # Cargo Tablero y configuracion
            if self.menu_principal == Menu_Principal.NUEVO_JUEGO:
                while True:
                    try:
                        valores = input('Ingrese el tamaño en formato "fila x columna":').split('x')
                        if len(valores) != 2 or not str(valores[0]).isnumeric() or not str(valores[1]).isnumeric():
                            raise FormatoIncorrecto('Las dimensiones del tablero requieren que sean expresadas en formato "fila x columna". Ej:5x5.')
                        else:
                            fila, columna = (int (x) for x in valores)
                            if fila > 30 or columna > 60:
                                raise FormatoIncorrecto('Las dimensiones del tablero no deben superar a 30x60.')
                            if fila < 3 or columna < 3:
                                raise FormatoIncorrecto('Las dimensiones del tablero deben superar a 3x3.')
                            self.tablero = Tablero(fila, columna)
                            break
                    except FormatoIncorrecto as e:
                        print(str(e))
            elif self.menu_principal == Menu_Principal.CARGAR_PARTIDA:
                try:
                    persistencia.printList()
                    self.tablero = persistencia.cargar(input('Ingrese el nombre de la partida:'))
                except IOError:
                    input('No se encontro una partida con ese nombre. Presione la tecla "Enter" para continuar...')
            elif self.menu_principal == Menu_Principal.SALIR:
                break #Cierro el programa
            self.limpiar()
            if self.tablero != None:
                #Cargo Configuraciones si no estan seteadas
                try:
                    if self.tablero.modo_de_juego == Modo_De_Juego.NOTSET:
                        self.tablero.modo_de_juego = (self.leer_entero('Seleccione el modo de juego: \n'
                                                                         '1 - Normal \n'
                                                                         '2 - Paso a paso \n' 
                                                                         '3 - Vida Estática \n' 
                                                                         '0 - Salir \n', True))
                    if self.tablero.modo_de_juego != Modo_De_Juego.VIDA_ESTATICA and \
                            self.tablero.modo_de_juego != Modo_De_Juego.NOTSET and \
                            self.tablero.modo_de_generacion == Modo_De_Generacion.NOTSET:
                        self.tablero.modo_de_generacion = self.leer_entero('Seleccione el método de generación: \n'
                                                                             '1 - Aleatorio \n'
                                                                             '2 - Manual \n' 
                                                                             '0 - Salir \n', True)
                        if self.tablero.modo_de_generacion == Modo_De_Generacion.RANDOM:
                            while True:
                                try:
                                    self.tablero.random(self.leer_entero('Ingresar número de células vivas:'))
                                    break
                                except IndexError as ex:
                                    print(str(ex))
                        elif self.tablero.modo_de_generacion == Modo_De_Generacion.MANUAL:
                            self.editar_tablero()
                        elif self.tablero.modo_de_generacion == Modo_De_Generacion.NOTSET:
                            break
                    elif self.tablero.modo_de_juego == Modo_De_Juego.VIDA_ESTATICA and self.tablero.celulas_random == 0:
                        while True:
                            try:
                                self.tablero.random(self.leer_entero('Ingresar número de células vivas:'))
                                break
                            except IndexError as ex:
                                print(str(ex))
                    elif self.tablero.modo_de_juego == Modo_De_Juego.NOTSET:
                        break
                    self.limpiar()
                    # Inicia el juego
                    print(self.tablero.impresion_tablero())
                    while True:
                        accion = None
                        if self.tablero.modo_de_juego == Modo_De_Juego.VIDA_ESTATICA:
                            self.tablero.vida_estatica()
                            input('Presione la tecla "Enter" para continuar...')
                            break
                        else:
                            if self.tablero.modo_de_juego == Modo_De_Juego.PASOAPASO:
                                accion = self.leer_entero('1 - Siguiente Generación \n'
                                                            '2 - Editar \n'
                                                            '3 - Guardar \n'
                                                            '0 - Salir \n', True)
                            if self.tablero.modo_de_juego == Modo_De_Juego.NORMAL or accion == Accion.SIGUENTE:
                                if self.tablero.modo_de_juego == Modo_De_Juego.NORMAL:
                                    time.sleep(0.1)
                                if self.tablero.finalizo:
                                    input('Se encontró un tablero estatico.' if self.tablero.estatico else 'El juego ha finalizado.' +
                                    '\nPresione la tecla "Enter" para volver al menú principal...')
                                    break
                                self.limpiar()
                                self.tablero.actualizar_celulas()
                                print(self.tablero.impresion_tablero())
                            elif accion == Accion.EDITAR:
                                self.editar_tablero()
                            elif accion == Accion.GUARDAR:
                                persistencia.guardar(self.tablero, input('Ingrese el nombre de la partida:'))
                            elif accion == Accion.SALIR:
                                break
                except IndexError:
                    input('Por favor ingresar un valor valido.\nPresione la tecla "Enter" para continuar...')
                except (KeyboardInterrupt):
                    persistencia.guardar(self.tablero, input('Ingrese el nombre de la partida:'))
                except Exception as ex:
                    input(str(ex) + '\nPresione la tecla "Enter" para continuar...')

    def editar_tablero(self):
        while True:
            try:
                valores = input('Ingresar coordenadas de la célula que desea modificar en formato "fila x columna":').split('x')
                if len(valores) != 2 or not str(valores[0]).isnumeric() or not str(valores[1]).isnumeric():
                    raise FormatoIncorrecto('Las coordenadas de la célula requieren que sean expresadas en formato "fila x columna". Ej:5x5.')
                else:
                    self.limpiar()
                    self.tablero.set_value(int(valores[0]), int(valores[1]))
                    print(self.tablero.impresion_tablero())
                    if self.leer_entero('1 - Modificar otra célula \n'
                                        '0 - Iniciar Juego \n') == 0:
                        break
            except IndexError:
                input('Las coordenadas exceden los limites del tablero. \n Presione la tecla "Enter" para continuar...')
            except (FormatoIncorrecto) as e:
                input(str(e) + ' \nPresione la tecla "Enter" para continuar...')
        self.limpiar()

    def leer_entero(self, texto, tomar_valores=False):
        valor = ''
        while valor == '':
            try:
                valor = input(texto)
                if valor == '' or not valor.isdigit():
                    raise IndexError('Por favor, ingrese un número.')
                valor = int(valor)
                if tomar_valores and not valor in [int(s) for s in texto.split() if s.isdigit()] and valor < 0:
                    raise IndexError('Por favor, ingrese un número correspondiente al menú:' + str([int(s) for s in texto.split() if s.isdigit()]))
                return valor
            except IndexError as ex:
                print(str(ex))
            valor = ''

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
