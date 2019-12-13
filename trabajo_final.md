## Introducción

El presente documento describe el código utilizado en el desarrollo de la aplicación Diccionario Quichua Santiagueño. La misma fue desarrollada luego de un pequeño trabajo de investigación, tanto en bibliografía como algunos tutoriales Online.
Uno de los apoyos fundamentales para este programa fue el tutorial de Tkinter + SQLite, al que puede accederse en este [link](https://www.youtube.com/watch?v=W2kAF9pKPPE). No tanto por lo que desarrolla sobre la librería Tkinter, ya que la vimos en profundidad en clase. Lo más interesante fue ver la manera en que el programador trabaja el software definiendo algunas funciones y desarrollando una clase (Class) central para el mismo. Además, permitió conocer algunas de las herramientas fundamentales de la librería sqlite3.
Desde la página web StackOverflow y desde la bibliografía oficial de Python se pudieron resolver varios de los problemas encontrados en el camino. También el libro “Python Crash Course” fue un documento de consulta recurrente.
Sin más, entramos directamente en el programa. La idea central consiste en un pequeño (y rudimentario) diccionario, que permita conocer el significado de algunas palabras en quichua. Además, debería permitir ver el listado de palabras, para poder editarlas, agregar algunas nuevas o incluso eliminarlas. A su vez, editar y agregar palabras requiere de una ventana particular para cada acción. Así que, en una Class que se denominó Diccionario fuimos desarrollando una a una las funciones necesarias para el programa.
A continuación, detallaremos estas funciones una por una. El orden elegido para la exposición es el de las ventanas que el potencial usuario de la aplicación se iría encontrando.

## Ventana principal

La ventana principal del programa se inicia luego de comprobar que el programa está siendo ejecutado en primer plano. Lo compruebo con las palabras reservadas \_\_name__ y \_\_main__. Lo hice de esta forma siguiendo las sugerencias de buenas prácticas en la programación orientada a objetos. De esta manera, se podrían importar algunas de las funciones de este programa a cualquier otro proyecto en Python sin mayores problemas. El código queda de la siguiente manera:

    if __name__ == '__main__':
        ventana = Tk()
        Diccionario(ventana)
        ventana.mainloop()

La ventana de TKinter es contenida en la variable del mismo nombre. Luego, la paso a la Class Diccionario, que veremos a continuación. Este pequeño bloque de código termina con el método mainloop, necesario para que la ventana de TKinter permanezca en ejecución.

Los contenidos de la ventana inicial son definidos dentro de la clase, cuyo encabezado es el siguiente:

    class Diccionario:

        db_name = 'diccionario.db'

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Diccionario Quichua Santiagueño')

  De esta manera, creamos la clase y dentro de su función \_\_init__ recibimos la ventana de TKinter, la asignamos a una variable self, para poder utilizarla en el resto de funciones de la Class Diccionario, y le colocamos un título.

  La primer variable definida especifica el nombre de nuestra base de datos, que fue creada en la misma carpeta donde está nuestro script principal (main.py).

  El código restante simplemente crea algunos objetos de Tkinter, de manera tal que la ventana termina de la siguiente forma:

![Ventana principal](/main.png)

Al hacer click en el botón buscar, apelamos a la siguiente función:

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

  Básicamente, definimos en un primer momento las órdenes que pasaremos a SQLite en la variable consulta. La variable palabra_buscada sirve para
