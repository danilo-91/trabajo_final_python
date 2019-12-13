from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import sqlite3

class Diccionario:

    db_name = 'diccionario.db'

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Diccionario Quichua Santiagueño')
        
        #Barra de búsqueda
        Label(text = 'Ingrese la palabra que desea buscar').grid(row = 0, column = 0, columnspan = 2, pady = 5, padx = 5)
        self.busqueda = Entry()
        self.busqueda.grid(row = 1, columnspan = 2)
        self.busqueda.focus_set()

        #Label de resultado
        Label(text = 'Definición').grid(row = 3, column = 0)
        self.definicion = Entry(textvariable = '', state = 'readonly')
        self.definicion.grid(row = 3, column = 1)

        #Botón buscar
        ttk.Button(text = 'Buscar', command = self.buscar).grid(row = 2, column = 0, sticky = W + E, pady = 5)

        #Botón para ver la lista de palabras
        ttk.Button(text = 'Ver lista de palabras', command = self.ver_lista).grid(row = 2, column = 1, sticky = W + E)

    def consultar_db(self, consulta, parametros = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result

    def buscar(self):
        consulta = 'SELECT definicion FROM diccionario WHERE palabra=?'
        palabra_buscada = self.busqueda.get()
        palabra_buscada = palabra_buscada.title()
        parametros = (palabra_buscada, )
        busco = self.consultar_db(consulta, parametros)
        rows = busco.fetchall()
        if len(rows) != 0:
            for row in rows:
                self.definicion['textvariable'] = StringVar(value = row)
        else:
            self.definicion['textvariable'] = StringVar(value = 'Palabra no encontrada')

    def actualizar_palabras(self):
        registro = self.lista.get_children()
        for element in registro:
            self.lista.delete(element)
        consulta = 'SELECT * FROM diccionario ORDER BY palabra DESC'
        filas_db = self.consultar_db(consulta)
        for row in filas_db:
            self.lista.insert('', 0, text= row[1], values = row[2])

    def validation(self):
        return len(self.nueva_palabra.get()) != 0 and len(self.nueva_definicion.get()) != 0 

    def comando_agregar_palabra(self):
        if self.validation():
            consulta = 'INSERT INTO diccionario VALUES(NULL, ?, ?)'
            palabra_en_mayuscula = self.nueva_palabra.get()
            palabra_en_mayuscula = palabra_en_mayuscula.title()
            parametros = (palabra_en_mayuscula, self.nueva_definicion.get())
            self.consultar_db(consulta, parametros)
            self.actualizar_palabras()
            self.agregar.destroy()
        else:
            messagebox.showerror('Error', 'Inserte un nombre y una definición válidos')

    def agregar_palabra(self):
        self.agregar = Toplevel()
        self.agregar.title('Agregar palabras')
        label1 = Label(self.agregar, text = 'Nueva palabra')
        label1.grid(row = 0, column = 0)
        self.nueva_palabra = Entry(self.agregar)
        self.nueva_palabra.grid(row = 0, column = 1)
        label2 = Label(self.agregar, text = 'Inserte la definición')
        label2.grid(row = 1, column = 0)
        self.nueva_definicion = Entry(self.agregar)
        self.nueva_definicion.grid(row = 1, column = 1)
        boton_agregar = Button(self.agregar, text = 'Agregar', command = self.comando_agregar_palabra)
        boton_agregar.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)

    def eliminar_palabra(self):
        try:
            self.lista.item(self.lista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror('Error', 'Elige la palabra que deseas eliminar')
            return
        palabra = self.lista.item(self.lista.selection())['text']
        consulta = 'DELETE FROM diccionario WHERE palabra=?'
        self.consultar_db(consulta, (palabra, ))
        self.actualizar_palabras()

    def editar_palabra(self):
        try:
            self.lista.item(self.lista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror('Error', 'Elige la palabra a editar')
            return
        palabra = self.lista.item(self.lista.selection())['text']
        definicion = self.lista.item(self.lista.selection())['values'][0]
        self.ventana_edit = Toplevel()
        self.ventana_edit.title('Editar palabra')

        #Palabra actual
        Label(self.ventana_edit, text = 'Palabra actual').grid(row = 0, column = 0, padx = 5)
        Entry(self.ventana_edit, textvariable = StringVar(self.ventana_edit, value = palabra), 
        state = 'readonly').grid(row = 0, column = 1, columnspan = 2)
        
        #Nombre nuevo
        Label(self.ventana_edit, text = 'Palabra nueva').grid(row = 1, column = 0)
        nueva_palabra = Entry(self.ventana_edit)
        nueva_palabra.grid(row = 1, column = 1)

        #Definición vieja
        Label(self.ventana_edit, text = 'Definición actual').grid(row = 2, column = 0)
        Entry(self.ventana_edit, textvariable = StringVar(self.ventana_edit, value = definicion), 
        state = 'readonly').grid(row = 2, column = 1, columnspan = 2)
        
        #Precio nuevo
        Label(self.ventana_edit, text = 'Nueva definición').grid(row = 3, column = 0)
        nueva_definicion = Entry(self.ventana_edit)
        nueva_definicion.grid(row = 3, column = 1)

        #Boton
        Button(self.ventana_edit, text = 'Actualizar', command = lambda: self.editar_db(nueva_palabra.get(), 
        nueva_definicion.get(), palabra, definicion)).grid(row = 4, columnspan = 2)

    def editar_db(self, nueva_palabra, nueva_definicion, vieja_palabra, vieja_definicion):
        consulta = 'UPDATE diccionario SET palabra = ?, definicion = ? WHERE palabra = ? AND definicion = ?'
        parametros = (nueva_palabra, nueva_definicion, vieja_palabra, vieja_definicion)
        self.consultar_db(consulta, parametros)
        self.ventana_edit.destroy()
        self.actualizar_palabras()

    def ver_lista(self):
        self.lista_de_palabras = Toplevel()
        self.lista_de_palabras.title('Lista de palabras en quichua')
        self.lista = ttk.Treeview(self.lista_de_palabras, height = 10, columns = 2)
        self.lista.grid(row = 1, column = 0, columnspan = 3)
        self.lista.heading('#0', text = 'Palabra', anchor = CENTER)
        self.lista.heading('#1', text = 'Definición', anchor = CENTER)
        self.actualizar_palabras()
        agregar = Button(self.lista_de_palabras, text = 'Agregar', command = self.agregar_palabra)
        agregar.grid(row = 2, column = 0, sticky = W + E)
        editar = Button(self.lista_de_palabras, text = 'Editar', command = self.editar_palabra)
        editar.grid(row = 2, column = 1, sticky = W + E)
        eliminar = Button(self.lista_de_palabras , text = 'Eliminar', command = self.eliminar_palabra)
        eliminar.grid(row = 2, column = 2, sticky = W + E)

if __name__ == '__main__':
    ventana = Tk()
    Diccionario(ventana)
    ventana.mainloop()