import shelve

class persistencia(object):

    def __init__(self):
        pass

    def guardar(self, ruta , tablero_celular, nombre):
        modulo_guardado = shelve.open(ruta)
        if not nombre in modulo_guardado:
           modulo_guardado[nombre] = tablero_celular
           modulo_guardado.close()
        else:
            modulo_guardado[nombre] = tablero_celular
            modulo_guardado.close()
        print("Tablero guardado con éxito.")


    def cargar(self, ruta, nombre):
        tablero_celular = None
        modulo_a_cargar = shelve.open(ruta)

        if modulo_a_cargar[nombre] != None:
            tablero_celular = modulo_a_cargar[nombre]
            print("Tablero cargado con éxito.")
            return tablero_celular