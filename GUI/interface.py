import tkinter as tk
from tkinter import *
from tkinter import messagebox

# Diccionario simulado de usuarios y contraseñas
users = {
    "bibliotecario": "password1",
    "cobros": "password2"
}

# Simulación de una base de datos en forma de diccionario JSON
database = { 
    "usuarios": [ 
        {"id": 1, "nombre": "Juan Pérez", "libros_alquilados": [101, 203], "fecha_alquiler":"20/08/2023"},
        {"id": 2,"nombre": "María García","libros_alquilados": [105, 307, 401],"fecha_alquiler":"15/01/2023"}
    ],
    "libros": [
        { "id": 101,"titulo": "Cien años de soledad","autor": "Gabriel García Márquez","disponible": False},
        { "id": 203,"titulo": "1984","autor": "George Orwell","disponible": False},
        { "id": 105,"titulo": "El principito","autor": "Antoine de Saint-Exupéry","disponible": False}
    ]
}

def db_checker(item_id, db_name):
    try:
        item_id = int(item_id)
    except ValueError:
        messagebox.showerror("Error", "Ingrese un ID válido.")
        return
        
    # Buscar el elemento en la base de datos
    found_item = None
    for item in database[db_name]:
        if item["id"] == item_id:
            found_item = item
            break

    return found_item

class LoginInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión")
        
        self.username_label = tk.Label(self, text="Usuario:")
        self.username_entry = tk.Entry(self)
        
        self.password_label = tk.Label(self, text="Contraseña:")
        self.password_entry = tk.Entry(self, show="*")
        
        self.login_button = tk.Button(self, text="Iniciar Sesión", command=self.login)
        
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username] == password:
            if username == "bibliotecario":
                self.destroy()
                consultas_interface = ConsultasInterface()
                consultas_interface.mainloop()
                # bibliotecario_interface = BibliotecarioInterface()
                # bibliotecario_interface.mainloop()
            elif username == "cobros":
                self.destroy()
                cobros_interface = CobrosInterface()
                cobros_interface.mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

# Implementación de la interfaz de "Bibliotecario nivel 1"
class BibliotecarioInterface(tk.Tk):
    def __init__(self, db_name):
        super().__init__()
        self.title("Bibliotecario Nivel 1")
        
        # Botones para CRUD y consulta
        self.create_button = tk.Button(self, text="Crear", command=lambda: self.create_item(db_name))
        self.read_button = tk.Button(self, text="Leer", command=lambda: self.read_item(db_name))
        self.update_button = tk.Button(self, text="Actualizar", command=lambda: self.update_item(db_name))
        self.delete_button = tk.Button(self, text="Borrar", command=lambda: self.delete_item(db_name))
        
        # Colocar los botones en la interfaz
        self.create_button.pack()
        self.read_button.pack()
        self.update_button.pack()
        self.delete_button.pack()

    # Lógica para crear un elemento en la base de datos
    def create_item(self, db_name):
        create_dialog = tk.Toplevel(self)
        create_dialog.title("Crear Nuevo Elemento")
        
        titulo_label = tk.Label(create_dialog, text="Título:")
        titulo_entry = tk.Entry(create_dialog)
        
        autor_label = tk.Label(create_dialog, text="Autor:")
        autor_entry = tk.Entry(create_dialog)

        disponible_label = tk.Label(create_dialog, text="Disponible:")
        variable = StringVar(create_dialog)
        variable.set("False") # default value
        disponible_entry = OptionMenu(create_dialog, variable, 'False', 'True')
        
        create_button = tk.Button(create_dialog, text="Crear", command=lambda: self.confirm_create(titulo_entry.get(), db_name, autor_entry.get(), disponible_entry, create_dialog))
        
        titulo_label.pack()
        titulo_entry.pack()
        autor_label.pack()
        autor_entry.pack()
        disponible_label.pack()
        disponible_entry.pack()
        create_button.pack()

    def confirm_create(self, db_name, new_title, new_author, new_state, create_dialog):
        new_id = max([item["id"] for item in database[db_name]], default=0) + 1
        new_item = {"id": new_id, "titulo": new_title, "autor": new_author, "disponible": new_state}
        database[db_name].append(new_item)
        create_dialog.destroy()
        messagebox.showinfo("Éxito", "Elemento creado correctamente con ID: "+str(new_id)+".")
    
    # Lógica para leer un elemento de la base de datos
    def read_item(self, db_name):
        # Ventana emergente para ingresar el ID del elemento a buscar
        input_dialog = tk.Toplevel(self)
        input_dialog.title("Buscar Elemento")
        
        id_label = tk.Label(input_dialog, text="ID del elemento:")
        id_entry = tk.Entry(input_dialog)
        search_button = tk.Button(input_dialog, text="Buscar", command=lambda: self.show_info(id_entry.get(), db_name))
        
        id_label.pack()
        id_entry.pack()
        search_button.pack()

    def show_info(self, item_id, db_name):
        found_item = db_checker(item_id, db_name)

        if found_item:
            info_dialog = tk.Toplevel(self)
            info_dialog.title("Información del Elemento")
            
            info_text = f"ID: {found_item['id']}\nTítulo: {found_item['titulo']}\nAutor: {found_item['autor']}\nEstado: {found_item['disponible']}"
            info_label = tk.Label(info_dialog, text=info_text)
            info_label.pack()
        else:
            messagebox.showerror("Error", "Elemento no encontrado.")
    
    # Lógica para actualizar un elemento en la base de datos
    def update_item(self, db_name):
        # Ventana emergente para ingresar el ID del elemento a actualizar
        input_dialog = tk.Toplevel(self)
        input_dialog.title("Actualizar Elemento")
        
        id_label = tk.Label(input_dialog, text="ID del elemento a actualizar:")
        id_entry = tk.Entry(input_dialog)
        update_button = tk.Button(input_dialog, text="Buscar", command=lambda: self.edit_element(id_entry.get(), db_name))
        
        id_label.pack()
        id_entry.pack()
        update_button.pack()

    # Lógica para actualizar un elemento de la base de datos
    def edit_element(self, item_id, db_name):
        found_item = db_checker(item_id, db_name)
        
        if found_item:
            edit_dialog = tk.Toplevel(self)
            edit_dialog.title("Editar Elemento")
            
            # Crear campos para editar información
            titulo_label = tk.Label(edit_dialog, text="Título:")
            titulo_entry = tk.Entry(edit_dialog)
            titulo_entry.insert(0, found_item["titulo"])
            
            autor_label = tk.Label(edit_dialog, text="Autor:")
            autor_entry = tk.Entry(edit_dialog)
            autor_entry.insert(0, found_item["autor"])

            disponible_label = tk.Label(edit_dialog, text="Disponible:")
            variable = StringVar(edit_dialog)
            variable.set(str(found_item["disponible"])) # default value
            disponible_entry = OptionMenu(edit_dialog, variable, 'False', 'True')

            update_button = tk.Button(edit_dialog, text="Actualizar", command=lambda: self.confirm_update(int(item_id), titulo_entry.get(), autor_entry.get(), disponible_entry, edit_dialog))

            titulo_label.pack()
            titulo_entry.pack()
            autor_label.pack()
            autor_entry.pack()
            disponible_label.pack()
            disponible_entry.pack()
            update_button.pack()
        else:
            messagebox.showerror("Error", "Elemento no encontrado.")

    def confirm_update(self, item_id, new_title, new_author, new_state, edit_dialog):
        for item in database["libros"]:
            if item["id"] == item_id:
                item["titulo"] = new_title
                item["autor"] = new_author
                if new_state == "False":
                    item["disponible"] = False
                else:
                    item["disponible"] = True

                edit_dialog.destroy()
                messagebox.showinfo("Éxito", "Elemento actualizado correctamente.")
                break
            else:
                messagebox.showerror("Error", "Elemento no encontrado.")

    # Lógica para borrar un elemento de la base de datos
    def delete_item(self, db_name):
        # Ventana emergente para ingresar el ID del elemento a borrar
        input_dialog = tk.Toplevel(self)
        input_dialog.title("Borrar Elemento")
        
        id_label = tk.Label(input_dialog, text="ID del elemento a borrar:")
        id_entry = tk.Entry(input_dialog)
        delete_button = tk.Button(input_dialog, text="Borrar", command=lambda: self.confirm_delete(id_entry.get(), db_name))
        
        id_label.pack()
        id_entry.pack()
        delete_button.pack()

    def confirm_delete(self, item_id, db_name):
        found_item = db_checker(item_id, db_name)

        if found_item:
            response = messagebox.askyesno("Confirmación", "¿Está seguro de que desea borrar este elemento?")
            if response:
                database["libros"].remove(found_item)
                messagebox.showinfo("Éxito", "Elemento borrado correctamente.")
        else:
            messagebox.showerror("Error", "Elemento no encontrado.")

class ConsultasInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultas de Información")
        
        # Botones para consultar información
        self.libros_button = tk.Button(self, text="Consultar Libros", command=lambda: self.crud('libros'))
        self.usuarios_button = tk.Button(self, text="Consultar Usuarios", command=lambda: self.crud('usuarios'))
        
        # Colocar los botones en la interfaz
        self.libros_button.pack()
        self.usuarios_button.pack()

    def crud(self, db_name):
        self.destroy()
        bibliotecario_interface = BibliotecarioInterface(db_name)
        bibliotecario_interface.mainloop()

# Implementación de la interfaz de "Servicio de cobros"
class CobrosInterface(tk.Tk):
    # ... (código previo)
    pass

# Crear y mostrar la interfaz de inicio de sesión
# login_interface = LoginInterface()
# login_interface.mainloop()
consultas_interface = ConsultasInterface()
consultas_interface.mainloop()