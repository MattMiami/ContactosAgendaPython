from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as MessageBox
import csv

#-----------------------------------------MENSAJES PARA EL USUARIO-------------------------------------------------------------------------
def noExiste(var):
    var_s = str(var)
    MessageBox.showinfo("Contacto no encontrado", var_s+ ' '+ "no existe")

def write_name():
    MessageBox.showinfo("Contacto no encontrado", "Tienes que insertar un nombre")

def write_contact():
    MessageBox.showinfo("Escribe un nombre de contacto", "Debes escribir un contacto para usar la opcion \"Añadir Contacto\"")

def delete_message(name):
    var_name = str(name)
    if var_name =='':
        write_name()
    else:
        search = MessageBox.askquestion("Eliminar concacto", "¿Esta seguro de que desea eliminar este contacts?\n"+var_name)
        if search == "yes":
            return True
        else:
            return False

def modify_message(contact):
    var_name = str(contact[0])
    var_surname = str(contact[1])
    var_phone = str(contact[2])
    search = MessageBox.askquestion("Modificar contacto", "Desea modificar este contacto: \n"+"Nombre: "+var_name+"\nApellido: "+var_surname+"\nTelefono: "+var_phone)
    if search == "yes":
        return True
    else:
        return False

#-----------------------------------------INTERFAZ GRÁFICA-------------------------------------------------------------------------
class App():
    def __init__(self, raiz):
        self.window = raiz

                                    #------El Menú----------
        barraMenu = Menu(self.window)
        self.window.config(menu = barraMenu)
        filemenu = Menu(barraMenu, tearoff = 0, bg="Light Blue")
        filemenu.add_command(label = "Todos los contactos", command = lambda: mostrar_contactos(), font=("Aldrich", "9", "bold"))
        filemenu.add_command(label="Cerrar Agenda", command = lambda: raiz.destroy(), font = ("Aldrich", "9", "bold"))
        barraMenu.add_cascade(label="Opciones", menu=filemenu)

                                    #------Paneles-------
        panelInfo = LabelFrame(self.window, bg = "#87CEFA")
        panelInfo.grid(row = 2, column = 0,sticky=N)

        panelBotones = LabelFrame(self.window, bg = "#87CEFA")
        panelBotones.grid(row=0, column=1,sticky=E)

        panelContactos = LabelFrame(self.window, bg="#87CEFA")
        panelContactos.grid(row=0, column=0,sticky=N)

                                    #------Cuadros de texto-------
        Label(panelInfo, text = 'Nombre', bg="#87CEFA", font=("Aldrich", "11", "normal")).grid(row=0, column=0)
        inbox_name = Entry(panelInfo, font=("Aldrich", "11", "normal"), width = 28)
        inbox_name.grid(row=1, column=0)
        inbox_name.focus()

        Label(panelInfo, text='Apellido', bg="#87CEFA", font=("Aldrich", "11", "normal")).grid(row=0, column=1)
        inbox_surname = Entry(panelInfo, font=("Aldrich", "11", "normal"), width=30)
        inbox_surname.grid(row=1, column=1)

        Label(panelInfo, text='Teléfono', bg="#87CEFA", font=("Aldrich", "11", "normal")).grid(row=0, column=2)
        inbox_phone = Entry(panelInfo, font=("Aldrich", "11", "normal"), width=20)
        inbox_phone.grid(row=1, column=2)

                                    # ------Botones-------
        btAdd = Button(panelBotones, command=lambda: agregar(), text='Añadir contacto', width=19)
        btAdd.configure(bg="#90EE90", cursor='hand2', font=("Aldrich", "10", "normal"))
        btAdd.grid(row=0, column=0, padx=2, pady=3, sticky=W + E)

        btBuscar = Button(panelBotones, command=lambda: buscar(), text='Buscar', width=19)
        btBuscar.configure(bg="#90EE90", cursor='hand2', font=("Aldrich", "10", "normal"))
        btBuscar.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        btLimpiar = Button(panelBotones, command=lambda: limpiar(), text='Limpiar agenda', width=19)
        btLimpiar.configure(bg="#90EE90", cursor='hand2', font=("Aldrich", "10", "normal"))
        btLimpiar.grid(row=2, column=0, padx=2, pady=3, sticky=W + E)

        btModificar = Button(panelBotones, command=lambda: modificar(), text='Modificar',width=19)
        btModificar.configure(bg="#90EE90", cursor='hand2', font=("Aldrich", "10", "normal"))
        btModificar.grid(row=3, column=0, padx=2, pady=3, sticky=W + E)

        btMostrar = Button(panelBotones, command=lambda: mostrar_contactos(), text='Mostrar contactos', width=19)
        btMostrar.configure(bg="#90EE90", cursor='hand2', font=("Aldrich", "10", "normal"))
        btMostrar.grid(row=4, column=0, padx=2, pady=3, sticky=W + E)

        btEliminar = Button(panelBotones, command=lambda: eliminar(), text='Eliminar', width=19)
        btEliminar.configure(bg="#F08080", cursor='hand2', font=("Aldrich", "10", "normal"))
        btEliminar.grid(row=5, column=0, padx=2, pady=3, sticky=W + E)

                                    #------Combo Boxes-------
        Label(panelBotones, text = 'Buscar/Modificar', bg="#87CEFA",font=("Aldrich", "10", "normal")).grid(row = 6, column = 0, columnspan = 3)

        combo = ttk.Combobox(panelBotones, state='readonly', width=17, justify='center', font=("Aldrich", "10", "normal"))
        combo["values"] = ['Nombre', 'Apellidos', 'Teléfono']
        combo.grid(row=7, column=0, padx=15)
        combo.current(0)

                                    #------Tabla de contactos--------
        self.tree=ttk.Treeview(panelContactos, heigh = 10, columns=("one","two"))
        self.tree.grid(padx = 5, pady = 5, row = 0, column = 0, columnspan = 1,sticky=N)
        self.tree.heading("#0", text='Nombre', anchor=CENTER)
        self.tree.heading("one", text='Apellidos', anchor=CENTER)
        self.tree.heading("two", text='Teléfono', anchor=CENTER)

                                    #-------Para el scroll de la tabla-----------
        scrollVert = Scrollbar(panelContactos, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollVert.set)
        scrollVert.grid(row=0, column=1, sticky="nsew")

        scroll_x = Scrollbar(panelContactos, command=self.tree.xview, orient=HORIZONTAL)
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=2, column=0, columnspan=1, sticky="nsew")

#----------------------------------FUNCIONES------------------------------------

        def _limpiar_texto():
            inbox_name.delete(0,"end")
            inbox_surname.delete(0, "end")
            inbox_phone.delete(0, "end")

        def _limpiar_lista():
            tree_list = self.tree.get_children()
            for item in tree_list:
                self.tree.delete(item)

        def _vista_csv():
            with open('contacts_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    name = str(row[0])
                    surname = str(row[1])
                    phone = str(row[2])
                    self.tree.insert("", 0, text = name, values = (surname, phone))

        def _guardar(name, surname, phone):
            g_name = name
            g_surname = surname
            g_phone = phone
            with open('contacts_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter = ',')
                writer.writerow((g_name, g_surname, g_phone))

        def _buscar(var_inbox, possition):
            list = []
            s_var_inbox = str(var_inbox)
            var_possition = int(possition)
            with open('contacts_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if s_var_inbox == row[var_possition]:
                        list = [row[0], row[1], row[2]]
                        break
                    else:
                        continue
            return list

        def _check(answer, var_search):
            list_answer = answer
            var_search = var_search
            if list_answer == []:
                noExiste(var_search)
            else:
                name = str(list_answer[0])
                surname = str(list_answer[1])
                phone = str(list_answer[2])
                self.tree.insert("", 0, text = "------------------------------", values = ("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text = name, values = (surname, phone))
                self.tree.insert("", 0, text = "Resultados nombres", values = ("Resultados apellidos", "Resultados teléfonos"))

        def _check1(answer, var_search):
            val_modify = answer
            var = var_search
            if val_modify == []:
                noExiste(var)
            else:
                VentanaModificar(self.window, val_modify)


                            #------------------------------------Funciones de los botones--------------------------------------------------------

        def agregar():
            name = inbox_name.get()
            surname = inbox_surname.get()
            phone = inbox_phone.get()
            contact_check = [name, surname, phone]
            if contact_check == ['','','']:
                write_contact()
            else:
                if name == '':
                    name = '<Default>'
                if surname == '':
                    surname = '<Default>'
                if phone == '':
                    phone = '<Default>'
                _guardar(name, surname, phone)
                self.tree.insert("", 0, text="------------------------------", values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=str(name), values=(str(surname), str(phone)))
                self.tree.insert("", 0, text="Nuevo nombre añadido", values=("Nuevo apellido añadido", "Nuevo telefono añadido"))
                self.tree.insert("", 0, text="------------------------------", values=("------------------------------", "------------------------------"))
            contact_check = []
            _limpiar_texto()

        def buscar():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = inbox_name.get()
                possition = 0
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)
            elif var_search == 'Apellido':
                var_inbox = inbox_surname.get()
                possition = 1
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)
            else:
                var_inbox = inbox_phone.get()
                possition = 2
                answer = _buscar(var_inbox, possition)
                _check(answer, var_search)

        def modificar():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = inbox_name.get()
                possition = 0
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            elif var_search == 'Apellido':
                var_inbox = inbox_surname.get()
                possition = 1
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            else:
                var_inbox = inbox_phone.get()
                possition = 2
                answer = _buscar(var_inbox, possition)
                _check1(answer, var_search)
            _limpiar_texto()

        def mostrar_contactos():
            _vista_csv()


        def eliminar():
            name = str(inbox_name.get())
            a = delete_message(name)
            if a == True:
                with open('contacts_list.csv', 'r') as f:
                    reader = list(csv.reader(f))
                with open('contacts_list.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                    for i, row in enumerate(reader):
                        if name != row[0]:
                            writer.writerow(row)
            limpiar()
            mostrar_contactos()

        def limpiar():
            _limpiar_texto()
            _limpiar_lista()

            #------Nueva clase para ventana modificar contacto--------
class VentanaModificar():
    def __init__(self, raiz, val_modify):
        self.raiz_window = raiz
        self.val_modify = val_modify
        self.name = str(self.val_modify[0])
        self.surname = str(self.val_modify[1])
        self.phone = str(self.val_modify[2])

        window_modify = Toplevel(self.raiz_window)
        window_modify.title("Modificar Contacto")
        window_modify.configure(bg = "#87CEFA")
        window_modify.geometry("615x130")
        window_modify.resizable(0,0)

        panel_texto = LabelFrame(window_modify, bg = "#87CEFA")
        panel_texto.grid(row=0, column=0)

        bt_panel_texto = LabelFrame(window_modify, bg = "#87CEFA")
        bt_panel_texto.grid(row=2, column=0)
                                # ------Dialogo de confirmacion-------------------
        Label(panel_texto, text = "¿Quieres modificar este contacto?", bg = "#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 0, column = 0, columnspan = 3)
        Label(panel_texto, text = self.name, bg = "#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 0)
        Label(panel_texto, text = self.surname, bg = "#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 1)
        Label(panel_texto, text = self.phone,bg = "#87CEFA", font = ("Alrich", "11", "normal")).grid(row = 1, column = 2)

                                #------Cuadros de texto ventana modificar-------------------
        Label(panel_texto, text = "Introduce un nuevo Nombre", bg = "#87CEFA",font = ("Alrich", "11", "normal")).grid(row = 2, column = 0)
        nombre = Entry(panel_texto, font = ("Alrich", "11", "normal"), width=25)
        nombre.grid(row = 3, column = 0)
        nombre.focus()

        Label(panel_texto, text="Introduce un nuevo Apellido", bg="#87CEFA", font=("Alrich", "11", "normal")).grid(row=2, column=1)
        ape = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        ape.grid(row=3, column=1)

        Label(panel_texto, text="Introduce un nuevo Teléfono", bg="#87CEFA", font=("Alrich", "11", "normal")).grid(row=2,column=2)
        tlf = Entry(panel_texto, font=("Alrich", "11", "normal"), width=25)
        tlf.grid(row=3, column=2)

                                #-------Botones----------------------------
        btOk = Button(bt_panel_texto, command = lambda: si(), text = "Si", width = 10)
        btOk.configure(bg = "#90EE90", cursor = 'hand2',font=("Alrich", "11", "normal"))
        btOk.grid(row = 1, column = 0, padx = 2, pady = 3, sticky = W + E)

        btNo = Button(bt_panel_texto, command = window_modify.destroy, text = "No",width = 10, bg = "yellow", cursor = 'hand2')
        btNo.configure(bg = "#90EE90", cursor = 'hand2', font=("Alrich", "11", "normal"))
        btNo.grid(row = 1, column = 1, padx = 2, pady = 3, sticky = W + E)

        btCancel = Button(bt_panel_texto, command = window_modify.destroy, text = "Cancelar", width = 10, bg = "green", cursor = 'hand2')
        btCancel.configure(bg = "#90EE90", cursor = 'hand2', font=("Alrich", "11", "normal"))
        btCancel.grid(row = 1, column = 2, padx = 2, pady = 3, sticky = W + E)

        #----Funciones de los botones-------

        def si():
            contact = self.val_modify
            nombre_nuevo = nombre.get()
            ape_nuevo = ape.get()
            tlf_nuevo = tlf.get()
            a = modify_message(contact)
            if a == True:
                _eliminar_antiguo(contact[0])
                _agregar_nuevo(nombre_nuevo, ape_nuevo, tlf_nuevo)
            window_modify.destroy()

        def _agregar_nuevo(nombre, apellido, tlf):
            g_nombre = nombre
            g_ape = apellido
            g_tlf = tlf
            with open('contacts_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                writer.writerow((g_nombre,g_ape,g_tlf))

        def _eliminar_antiguo(nombre_antiguo):
            nombre = nombre_antiguo
            with open('contacts_list.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('contacts_list.csv','w') as f:
                writer = csv.writer(f, lineterminator ='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if nombre != row[0]:
                        writer.writerow(row)






