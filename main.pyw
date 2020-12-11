from tkinter import *
import contactos

def main():
    raiz = Tk()
    raiz.title("Agenda de contactos")
    raiz.iconbitmap("contactos.ico")
    raiz.config(bg="Light Blue")
    raiz.geometry("820x350")
    raiz.resizable(0, 0)
    contactos.App(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()