from tkinter import *

class Juego_de_la_Vida(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("Juego de la Vida")
        self.resizable(width=False, height=False)
        SimpleTable(self, 20, 20)

class SimpleTable(Frame):
    def __init__(self, parent, rows=10, columns=10):
        # Fondo negro
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                # En cada celda cargo un boton que al precionar llama a set
                boton_celula = Button(self, text="", borderwidth=0, width=2, bg="White",
                                      command=lambda row=row, col=column: self.set(row, col))
                boton_celula.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(boton_celula)
            self._widgets.append(current_row)
        self.pack(fill="both", expand ="True")

    def set(self, row, column, value=""):
        # Obtengo la celda por row y column
        widget = self._widgets[row][column]
        if value != "": # Si recibo color, lo ingreso
            widget.configure(bg=value)
        elif widget.cget("bg") == 'White':
            widget.configure(bg="Red")
        else: # En caso de no recibir color, toggle entre Blanco y Rojo
            widget.configure(bg="White")

if __name__ == "__main__":
    app = Juego_de_la_Vida()
    app.mainloop()