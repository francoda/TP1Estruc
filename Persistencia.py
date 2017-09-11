import shelve

class persistencia(object):

    def __init__(self):
        pass

    @staticmethod
    def guardar(ruta , tablero_celular, nombre):
        modulo_guardado = shelve.open(ruta)
        modulo_guardado[nombre] = tablero_celular
        modulo_guardado.close()
        print("Tablero guardado con éxito.")

    @staticmethod
    def cargar(ruta, nombre):
        modulo_a_cargar = shelve.open(ruta)

        if modulo_a_cargar[nombre] != None:
            tablero_celular = modulo_a_cargar[nombre]
            print("Tablero cargado con éxito.")
            return tablero_celular