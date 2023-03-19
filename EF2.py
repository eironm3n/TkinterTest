# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter import ttk
import sqlite3
import re

# Desarrollo de la Interfaz Gráfica #
root = Tk()
root.title("Stock All")
# --> Titulo de la ventana
root.geometry("600x350")
# --> Dimensiones de la ventana

var_id = StringVar()
var_producto = StringVar()
var_cantidad = IntVar()
var_precio = IntVar()


def conexionBD():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute(
            """
        CREATE TABLE planilla(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PRODUCTO VARCHAR(100) NOT NULL,
        CANTIDAD INT(4) NOT NULL,
        PRECIO INT NOT NULL)
        """
        )
        messagebox.showinfo("CONEXION", "Base de Datos Creada exitosamente")
    except:
        messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")


def eliminarBD():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    if messagebox.askyesno(
        message="Los datos se perderan definitivamente, ¿Desea continuar?",
        tittle="ADVERTENCIA",
    ):
        miCursor.execute("DROP TABLE planilla")
    else:
        pass
    limpiarCampos()
    mostrar()


# En el caso de que quieran eliminar la base de datos creada


def salirAplicacion():
    valor = messagebox.askquestion(
        "Salir", "Esta seguro que desea salir de la aplicación"
    )
    if valor == "yes":
        root.destroy()


# Para cerar la aplicación


def limpiarCampos():
    var_id.set("")
    var_producto.set("")
    var_cantidad.set("")
    var_precio.set("")


# Para limpiar los campos


def mensaje():
    acerca = """
    Aplicación CRUD
    Version 1.0
    Tecnología Python Tkinter
    """
    messagebox.showinfo(title="INFORMACIÓN", message=acerca)


# Es para mostrar la información de la librería que utilizamos dentro del lenguaje

################################ MODELO(CRUD) #############################################
def crear():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        datos = var_producto.get(), var_cantidad.get(), var_precio.get()
        miCursor.execute("INSERT INTO planilla VALUES(NULL,?,?,?)", datos)
        miConexion.commit()
    except:
        messagebox.showwarning("AVERTENCIA", "Ocurrió un error al crear el registro")
        pass
    # Si sale este error, es por que tuvo un inconveniente al crear el registro
    limpiarCampos()
    mostrar()


def mostrar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    # el elemento get_children permite traer los elementos de la tabla
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT * FROM planilla")
        for row in miCursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))
    except:
        pass


################################ VISTA(Tabla) #############################################
tree = ttk.Treeview(height=10, columns=("#0", "#1", "#2", "#3"))
tree.place(x=0, y=130)
tree.column("#0", width=100)
tree.heading("#0", text="ID", anchor=CENTER)
tree.heading("#1", text="Producto", anchor=CENTER)
tree.heading("#2", text="Cantidad", anchor=CENTER)
tree.column("#3", width=100)
tree.heading("#3", text="Precio ($)", anchor=CENTER)


def seleccionarUsandoClick(event):
    item = tree.identify("item", event.x, event.y)
    var_id.set(tree.item(item, "text"))
    var_producto.set(tree.item(item, "values")[0])
    var_cantidad.set(tree.item(item, "values")[1])
    var_precio.set(tree.item(item, "values")[2])


tree.bind("<Double-1>", seleccionarUsandoClick)


def actualizar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        datos = var_producto.get(), var_cantidad.get(), var_precio.get()
        miCursor.execute(
            "UPDATE planilla SET PRODUCTO=?, CANTIDAD=?, PRECIO=? WHERE ID="
            + var_id.get(),
            (datos),
        )
        miConexion.commit()
    except:
        messagebox.showwarning(
            "AVERTENCIA", "Ocurrió un error al actualizar el registro"
        )
        pass
    limpiarCampos()
    mostrar()


def borrar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        if messagebox.askyesno(
            message="¿Realmente desea eliminar el registro?", tittle="ADVERTENCIA"
        ):
            miCursor.execute("DELETE FROM planilla WHERE ID=" + var_id.get())
            miConexion.commit()
    except:
        messagebox.showwarning("AVERTENCIA", "Ocurrió un error al eliminar el registro")
        pass
    limpiarCampos()
    mostrar()


################################ CONTROLADOR(widgets) #############################################
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBD)
# Se agrega un submenu que arroje la conexión "conexionBD" que creamos anteriormente
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBD)
# Se agrega un submenu que arroje la eliminación , utilizando la funcion que creamos anteriormente
menubasedat.add_command(label="Salir", command=salirAplicacion)
# Se agrega un submenu que arroje el 'exit' con la función que creamos anteriormente
menubar.add_cascade(label="Inicio", menu=menubasedat)


ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca de..", command=mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

#####################Etiquetas y cajas de texto########################
e1 = Entry(root, textvariable=var_id)

l2 = Label(root, text="Producto")
l2.place(x=50, y=10)
e2 = Entry(root, textvariable=var_producto, width=50)
e2.place(x=110, y=10)

l3 = Label(root, text="Cantidad")
l3.place(x=50, y=40)
e3 = Entry(root, textvariable=var_cantidad)
e3.place(x=110, y=40)

l4 = Label(root, text="Precio")
l4.place(x=280, y=40)
e4 = Entry(root, textvariable=var_precio, width=10)
e4.place(x=320, y=40)

l5 = Label(root, text="$")
l5.place(x=380, y=40)
#####################Creando Botones########################
b1 = Button(root, text="Crear Registro", command=crear)
b1.place(x=50, y=90)
b2 = Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=180, y=90)
b3 = Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=320, y=90)
b1 = Button(root, text="Eliminar Registro", bg="red", command=borrar)
b1.place(x=420, y=90)


root.config(menu=menubar)

root.mainloop()
