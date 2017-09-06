from tkinter import *

class Juego_de_la_Vida(Tk):
    def __init__(self):
        Tk.__init__(self)
        t = SimpleTable(self, 20,20)
        t.pack(fill="both", expand ="True")
        t.set(0,0,"Red")

class SimpleTable(Frame):
    def __init__(self, parent, rows=10, columns=10):
        # Fondo negro
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                boton_celula = Button(self, text="", borderwidth=0, width=2, bg="White")
                boton_celula.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(boton_celula)
            self._widgets.append(current_row)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(bg=value)

if __name__ == "__main__":
    app = Juego_de_la_Vida()
    app.mainloop()