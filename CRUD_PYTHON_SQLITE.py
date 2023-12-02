"""
El código proporcionado es una aplicación de interfaz gráfica de usuario (GUI).
Que permite administrar registros de usuarios en una base de datos SQLite. 
La aplicación utiliza la biblioteca Gtk para crear la GUI.
El código comienza importando los módulos necesarios, 
    subprocess para ejecutar comandos del sistema
    sqlite3 para conectarse a la base de datos SQLite
    gi para la biblioteca Gtk.

A continuación
se define la función "conectar_bd" 
que se utiliza para establecer una conexión con la base de datos. 
Si la conexión es exitosa, se imprime un mensaje de éxito
y se devuelve el objeto de conexión. 

Si hay un error al conectar a la base de datos
se imprime un mensaje de error y se devuelve None.

La función "mostrar_todos_registros" se utiliza para mostrar todos los registros de usuarios en el TreeView.
Primero, se establece una conexión con la base de datos llamando a la función "conectar_bd". 
Si la conexión es exitosa
    se ejecuta una consulta SELECT para obtener todos los registros de la tabla "users" 
    ordenados por apellido. 
    Los registros obtenidos se agregan al ListStore asociado al TreeView.

La función "on_search_changed" se llama cuando el texto en el campo de búsqueda cambia. 
Primero, se obtiene el texto de búsqueda. 
Si el texto no está vacío
    se establece una conexión con la base de datos llamando a la función "conectar_bd".
    Si la conexión es exitosa, se ejecuta una consulta 
        SELECT utilizando el texto de búsqueda para filtrar los registros por apellido.
        Los registros obtenidos se agregan al ListStore asociado al TreeView. Además, se desactivan los botones de editar y eliminar. Si el texto de búsqueda está vacío, se llama a la función "mostrar_todos_registros" para mostrar todos los registros y se desactivan los botones de editar y eliminar.

La función "on_row_activated" se llama cuando se hace clic en una fila del TreeView. 

La función "on_key_press_event" se llama cuando se presiona una tecla en el TreeView. 
Si la tecla presionada no es ENTER
    se muestra un cuadro de diálogo con un mensaje informativo.
Si es ENTER o Double Click 
    Se obtiene la selección actual y se obtienen los valores de la fila seleccionada.
    se activan los botones de editar y eliminar,  se imprime el registro seleccionado
    En la consola

La función "on_button_new_clicked" 
se llama cuando se hace clic en el botón de nuevo usuario. 
Se muestra un cuadro de diálogo con campos para ingresar los datos del nuevo usuario.
Si se hace clic en OK, 
    se inserta un nuevo registro en la base de datos utilizando la función "conectar_bd". 
    Luego, se llama a la función "mostrar_todos_registros" para actualizar el TreeView.

La función "on_button_edit_clicked" se llama cuando se hace clic en el botón de editar. 
Se obtiene la selección actual del TreeView 
y se muestra un cuadro de diálogo con los campos de edición. 
Si se hace clic en OK, se obtienen los nuevos valores y se actualiza el registro
en la base de datos utilizando la función "conectar_bd". 
Luego, se llama a la función "mostrar_todos_registros" para actualizar el TreeView.

La función "on_button_delete_clicked" se llama cuando se hace clic en el botón de eliminar. 
Se obtiene la selección actual del TreeView y se elimina el registro correspondiente 
se llama a la función "mostrar_todos_registros" para actualizar el TreeView.

La función "on_button_exit_clicked" se llama cuando se hace clic en el botón de salida. 
Cierra la aplicación.

En resumen, el código proporcionado es una aplicación de GUI que permite administrar registros de usuarios en una base de datos SQLite. Los registros se pueden buscar, agregar, editar y eliminar utilizando la interfaz gráfica proporcionada.
"""
import subprocess
import sqlite3
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def conectar_bd():
    try:
        conn = sqlite3.connect("appregistro.db")
        print("Conexión exitosa")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def mostrar_todos_registros(liststore):
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY lastname")
        rows = cursor.fetchall()
        liststore.clear()
        for row in rows:
            liststore.append(row)
        
    
def on_search_changed(entry, liststore, button_edit, button_delete):
    buscar_entry = entry.get_text()
    if buscar_entry.strip():
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE lastname LIKE ? || '%'", (buscar_entry,))
            rows = cursor.fetchall()
            liststore.clear()
            for row in rows:
                liststore.append(row)
            button_edit.set_sensitive(False)
            button_delete.set_sensitive(False)
    else:
        mostrar_todos_registros(liststore)
        button_edit.set_sensitive(False)
        button_delete.set_sensitive(False)

def on_row_activated(treeview, path, column, button_edit, button_delete):
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    if iter is not None:
        list_sel_reg = []
        for i in range(5):
            value = model.get_value(iter, i)
            list_sel_reg.append(value)
        print("Registro seleccionado:", list_sel_reg)
        button_edit.set_sensitive(True)
        button_delete.set_sensitive(True)

def on_key_press_event(treeview, event, button_edit, button_delete):
    if event.keyval != Gdk.KEY_Return:  # Verificar si la tecla presionada no es ENTER
        dialog = Gtk.MessageDialog(parent=None, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text="Por favor presione ENTER para seleccionar un registro o haga doble clic con el botón izquierdo del mouse.")
        dialog.run()
        dialog.destroy()
    return False

def on_button_new_clicked(button):
    dialog = Gtk.Dialog(title="Nuevo Usuario", parent=window, flags=0,
                        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK))

    grid = Gtk.Grid()
    grid.set_column_spacing(10)
    grid.set_row_spacing(10)
    dialog.get_content_area().add(grid)

    nombre_entry = Gtk.Entry()
    apellido_entry = Gtk.Entry()
    email_entry = Gtk.Entry()
    genero_combo = Gtk.ComboBoxText()
    genero_combo.append_text("Masculino")
    genero_combo.append_text("Femenino")
    edad_spin = Gtk.SpinButton()
    edad_spin.set_range(0, 150)

    grid.attach(Gtk.Label(label="Nombre:"), 0, 0, 1, 1)
    grid.attach(nombre_entry, 1, 0, 1, 1)
    grid.attach(Gtk.Label(label="Apellido:"), 0, 1, 1, 1)
    grid.attach(apellido_entry, 1, 1, 1, 1)
    grid.attach(Gtk.Label(label="Email:"), 0, 2, 1, 1)
    grid.attach(email_entry, 1, 2, 1, 1)
    grid.attach(Gtk.Label(label="Género:"), 0, 3, 1, 1)
    grid.attach(genero_combo, 1, 3, 1, 1)
    grid.attach(Gtk.Label(label="Edad:"), 0, 4, 1, 1)
    grid.attach(edad_spin, 1, 4, 1, 1)

    dialog.show_all()
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        nombre = nombre_entry.get_text()
        apellido = apellido_entry.get_text()
        email = email_entry.get_text()
        genero = genero_combo.get_active_text()
        edad = int(edad_spin.get_value())

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, lastname, email, gender, age) VALUES (?, ?, ?, ?, ?)",
                           (nombre, apellido, email, genero, edad))
            conn.commit()
            mostrar_todos_registros(liststore)

    dialog.destroy()

def on_button_edit_clicked(button):
    selection = tree_view.get_selection()
    model, iter = selection.get_selected()
    if iter is not None:
        list_sel_reg = []
        for i in range(5):
            value = model.get_value(iter, i)
            list_sel_reg.append(value)

        dialog = Gtk.Dialog(title="Editar Usuario", parent=window, flags=0,
                            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OK, Gtk.ResponseType.OK))

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        dialog.get_content_area().add(grid)

        nombre_entry = Gtk.Entry()
        apellido_entry = Gtk.Entry()
        email_entry = Gtk.Entry()
        genero_combo = Gtk.ComboBoxText()
        genero_combo.append_text("Masculino")
        genero_combo.append_text("Femenino")
        edad_spin = Gtk.SpinButton()
        edad_spin.set_range(0, 150)

        nombre_entry.set_text(list_sel_reg[0])
        apellido_entry.set_text(list_sel_reg[1])
        email_entry.set_text(list_sel_reg[2])
        genero_combo.set_active_id(list_sel_reg[3])
        edad_spin.set_value(int(list_sel_reg[4]))

        grid.attach(Gtk.Label(label="Nombre:"), 0, 0, 1, 1)
        grid.attach(nombre_entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="Apellido:"), 0, 1, 1, 1)
        grid.attach(apellido_entry, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label="Email:"), 0, 2, 1, 1)
        grid.attach(email_entry, 1, 2, 1, 1)
        grid.attach(Gtk.Label(label="Género:"), 0, 3, 1, 1)
        grid.attach(genero_combo, 1, 3, 1, 1)
        grid.attach(Gtk.Label(label="Edad:"), 0, 4, 1, 1)
        grid.attach(edad_spin, 1, 4, 1, 1)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            nombre = nombre_entry.get_text()
            apellido = apellido_entry.get_text()
            email = email_entry.get_text()
            genero = genero_combo.get_active_text()
            edad = int(edad_spin.get_value())

            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name = ?, lastname = ?, email = ?, gender = ?, age = ? WHERE name = ? AND lastname = ? AND email = ? AND gender = ? AND age = ?",
                               (nombre, apellido, email, genero, edad, list_sel_reg[0], list_sel_reg[1], list_sel_reg[2], list_sel_reg[3], list_sel_reg[4]))
                conn.commit()
                mostrar_todos_registros(liststore)
        
        button_edit.set_sensitive(False)
        button_delete.set_sensitive(False)
        dialog.destroy()

def on_button_delete_clicked(button):
    selection = tree_view.get_selection()
    model, iter = selection.get_selected()
    if iter is not None:
        list_sel_reg = []
        for i in range(5):
            value = model.get_value(iter, i)
            list_sel_reg.append(value)

        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE name = ? AND lastname = ? AND email = ? AND gender = ? AND age = ?",
                           (list_sel_reg[0], list_sel_reg[1], list_sel_reg[2], list_sel_reg[3], list_sel_reg[4]))
            conn.commit()
            mostrar_todos_registros(liststore)
    button_edit.set_sensitive(False)
    button_delete.set_sensitive(False)

def on_button_exit_clicked(button):
    Gtk.main_quit()

window = Gtk.Window(title="Registros de la tabla users")
window.set_border_width(10)
window.set_default_size(600, 550)
window.set_position(Gtk.WindowPosition.CENTER)
window.set_resizable(False)
window.connect("destroy", Gtk.main_quit)

layout = Gtk.Grid()
layout.set_column_spacing(10)
layout.set_row_spacing(10)
window.add(layout)

buscar_entry = Gtk.Entry()
buscar_entry.set_text("")
layout.attach(Gtk.Label(label="Buscar Usuarios:"), 0, 1, 1, 1)
layout.attach(buscar_entry, 1, 1, 1, 1)

liststore = Gtk.ListStore(str, str, str, str, int)
tree_view = Gtk.TreeView(model=liststore)

for i, column_title in enumerate(["Nombre", "Apellido", "Email", "Género", "Edad"]):
    renderer_text = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(column_title, renderer_text, text=i)
    tree_view.append_column(column)

# Agregar barras de desplazamiento al TreeView
tree_view.set_vexpand(True)
tree_view.set_hexpand(True)

# Establecer dimensiones para el TreeView
tree_view.set_size_request(600, 400)

layout.attach(tree_view, 0, 2, 2, 1)
 
mostrar_todos_registros(liststore)

# Botones con imágenes
buttons = Gtk.Grid()
buttons.set_column_homogeneous(True)
buttons.set_column_spacing(10)
layout.attach(buttons, 0, 3, 2, 1)

button_new = Gtk.Button()
image_new = Gtk.Image.new_from_icon_name("document-new", Gtk.IconSize.BUTTON)
button_new.set_image(image_new)
button_new.connect("clicked", on_button_new_clicked)
buttons.attach(button_new, 0, 0, 1, 1)

button_edit = Gtk.Button()
image_edit = Gtk.Image.new_from_icon_name("document-edit", Gtk.IconSize.BUTTON)
button_edit.set_image(image_edit)
button_edit.connect("clicked", on_button_edit_clicked)
buttons.attach(button_edit, 1, 0, 1, 1)
button_edit.set_sensitive(False)

button_delete = Gtk.Button()
image_delete = Gtk.Image.new_from_icon_name("edit-delete", Gtk.IconSize.BUTTON)
button_delete.set_image(image_delete)
button_delete.connect("clicked", on_button_delete_clicked)
buttons.attach(button_delete, 2, 0, 1, 1)
button_delete.set_sensitive(False)

button_exit = Gtk.Button()
image_exit = Gtk.Image.new_from_icon_name("application-exit", Gtk.IconSize.BUTTON)
button_exit.set_image(image_exit)
button_exit.connect("clicked", on_button_exit_clicked)


buscar_entry.connect("changed", on_search_changed, liststore, button_edit, button_delete)
tree_view.connect("row-activated", on_row_activated, button_edit, button_delete)
tree_view.connect("key-press-event", on_key_press_event, button_edit, button_delete)




buttons.attach(button_exit, 3, 0, 1, 1)

window.show_all()
Gtk.main()
