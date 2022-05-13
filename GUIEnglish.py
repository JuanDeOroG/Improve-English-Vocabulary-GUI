import random
import keyboard
import win32com.client as wincl
from tkinter import * 
from tkinter import ttk
import tkinter
from pyautogui import prompt
import sqlite3
from tkinter.font import Font


#Lector de texto (verbo o frase)
lector = 1
bocina = wincl.Dispatch("SAPI.SpVoice")
vcs = bocina.GetVoices()
bocina.voice
bocina.SetVoice(vcs.Item(lector))  # Lector numero 1 (ingles)

#Coneccion con base de datos
miconexion = sqlite3.connect("CajadePalabras")
micursor=miconexion.cursor()




listadegrupo=[] #Lista para almacenar grupo de palabras

import time
from typing import TypeVar
#Colores y letra
azul = "#115cb3"
rojo = "#f61743"
letra="Lato"
#Ventana inicial
root= Tk()
root.title("Evaluador de Inglés")
root.geometry("520x660")
root.resizable(0,0)
root.config(bg=azul)




# FRAME ROJO
miframe=Frame()
miframe.pack()
miframe.config(bg=rojo)
miframe.config(width=500, height=650 )

fondo = tkinter.PhotoImage(file="fondorayas.png")



titulo1 = Label(miframe, text="English evaluator", bg=azul, fg="white")
titulo1.place(x=0, y=1)
titulo1.config(font=(letra, 13,"bold"),padx=180)

#Generar texto de input
palabra = Label(miframe, text="Palabra/Word", bg=azul, fg="white")
palabra.place(x=3, y=60)
palabra.config(font=("Lato", 12))


#Texto y entrey de grupo de palabras
grupo = Label(miframe, text="Grupo/Group", bg=azul, fg="white", font=(letra,35))
grupo.place(x=10, y=100)
grupo.config(font=(letra, 12))
entry_grupo = Entry(miframe, bg="white", fg=azul, font=16)
entry_grupo.place(x=113, y=100)


#Separador estrategico para un diseño esperado
espacio = Label(miframe, text="      ",bg=azul,fg="white", padx=270, pady=10)
espacio.place(x=0, y=200)
espacio.config(font=20)

#Texto "Elegir Grupo"
evaluar = Label(miframe, text="Elegir Grupo       ", bg=azul,fg="white",font=30)
evaluar.place(x=73, y=207)


#Combo/despliegue de grupos de palabras o frases
combo = ttk.Combobox(miframe, state="readonly")
combo.place(x=200,y=209)


#evisar nombre de grupos
revisar=micursor.execute(f"SELECT name FROM sqlite_master WHERE type = 'table';")
gruponuevo=[]
for x in revisar:
    gruponuevo.append(x)

#Creando despliegue/combo segun la lista 'gruponuevo'    
grupos=combo["values"]= gruponuevo



def eliminartabla(): #Funcio para eliminar una tabla/grupo de el comobox/despliegue
    nametabla = combo.get() #Almacenar en nametabla el grupo seleccionado.
    armar = f"('{nametabla}',)"

    firstCont=0
    contador = 0

    for x in gruponuevo:
        if nametabla in str(x):
            gruponuevo.pop(firstCont)
            
        firstCont += 1
        contador += 1
    
    delete = f"DROP TABLE {nametabla};" #Creando consulta para eliminar tabla seleccionada
    miconexion.commit() 
    mandar = micursor.execute(delete) #Eliminar tabla con nombre almacenado en "nametabla"
    grupos = combo["values"] = gruponuevo #Actualizar lista de grupos

#Crear botón para eliminar tabla seleccionada en combobox/despliegue
boton_mostrar = Button(miframe, text="Eliminar", command=eliminartabla)
boton_mostrar.place(x=10, y=320)
boton_mostrar.config(font=(letra, 12, "bold"), bg=azul, fg="white")



def agregar_grupo(): #Funcion para agregar un nuevo grupo de palabras
    #crear pestaña en la GUI
    nombre_grupo = prompt(text='Digite el nombre del grupo', title='Crear Grupo', default='')

    #Añadir tabla/grupo a la base de datos
    consulta = f"CREATE TABLE {nombre_grupo}(palabras varchar(50))"
    try:lista=micursor.execute(consulta);miconexion.commit()
    except:print("Error, ya existe una tabla con ese nombre") 

    #añadir nombre de grupo al combobox
    consulta2 = f"SELECT name FROM sqlite_master WHERE type = 'table';"
    tablas=micursor.execute(consulta2)
    sacadas=[] #Lista para almacenar grupos ya creados
    for x in tablas:
        sacadas.append(x) #agregar para identificar a los grupos ya creados

    if nombre_grupo in sacadas: #Comprobar si el grupo digitado ya está creado
        print(f"El grupo {x} ya está dentro") #Aquí se puede crear un mensaje de error
    else: 
        gruponuevo.append(nombre_grupo)
        grupos = combo["values"] = gruponuevo
    


#Menu/pestaña de crear grupo-------------------
menuBar = Menu(root)
root.config(menu=menuBar)
addgrupo = Menu(menuBar, tearoff=0)
addgrupo.add_command(label="Agregar Nuevo Grupo", command=agregar_grupo)
menuBar.add_cascade(label="Crear Grupos", menu=addgrupo)



#Cuadro para mostrar las palabras que contiene el grupo seleccionado.
lista1 = Listbox(miframe, width=18,height=8, borderwidth=10, bg=azul, fg="#fff", selectforeground="#ffffff",
                 selectbackground=rojo, selectborderwidth=3, font=Font(family="Sans Serif", size=20))
lista1.place(x=95, y=280)


def mostrar(): #Funcion para mostrar en el cuadro el contenido del grupo seleccionado 

    gruposeleccionado=combo.get()
    lista1 = Listbox(miframe, width=18, height=8, borderwidth=10, bg=azul, fg="#fff", selectforeground="#ffffff",
                     selectbackground=rojo, selectborderwidth=3, font=Font(family="Sans Serif", size=20))
    lista1.place(x=95, y=280)
    orden = f"SELECT palabras FROM {gruposeleccionado}"
    ejecutar=micursor.execute(orden)

    cantidad_palabras=0 #Variable para guardar cuantas palabras hemos aprendido en total

    for x in ejecutar:  # Para limpiar texto, quitar parentesis, comas, etc...
        cantidad_palabras += 1
        y=str(x)
        lean=y.replace("'","")
        leanA=lean.replace("(","")
        leanB = leanA.replace(")", "")
        leanC = leanB.replace(",", "")
        lista1.insert(cantidad_palabras, leanC)

    

#Boton para mostrar contenido de grupo seleccionado
boton_mostrar = Button(miframe, text="Mostrar", command=mostrar)
boton_mostrar.place(x=10, y=280)
boton_mostrar.config(font=(letra, 12,"bold"), bg=azul, fg="white")


def evaluargrupo(): #Funcion para ventana de evaluación de palabras
    seleccion=combo.get()
    # print(seleccion)
    ejecutar = f"SELECT palabras FROM {seleccion}"
    ejecutarcomando= micursor.execute(ejecutar)
    
    for x in ejecutarcomando: #Limpiar texto
        xstr=str(x)
        
        lean1=xstr.replace("(","")
        lean2=lean1.replace(")", "")
        lean3=lean2.replace(",", "")
        lean4=lean3.replace("'", "")
        lean5=lean4.replace("'", "")
        
        listadegrupo.append(lean5)
    
    
    ventananueva = Toplevel() #Crear Ventana hija
    ventananueva.geometry("440x660")
    ventananueva.config(background=azul)
    listaY=[1,0]
    listaX=[1,0]
    def ponerpalabra(): #Para continuar a evaluar la siguiente palabra
        
        uno=1
        wordRandom = random.choice(listadegrupo) #Elegir palabra aleatoriamente
        posword = listadegrupo.index(wordRandom)
    
        suma = sum(listaY)
        if suma == 11: #Condicional para mejor diseño de la ventana
            listaY.clear()
            capa = Label(ventananueva, bg=azul,
                         borderwidth=4)
            capa.config(pady=300, padx=120)
            capa.place(x=0, y=0)
        palabras= Label(ventananueva, text=f"{wordRandom}")
        listadegrupo.pop(posword)
        palabras.config(font=(letra, 20), padx=5, background="white",
                        borderwidth=4, relief="raised", fg=azul)
        palabras.grid(row=suma,column=1)
        
    
        if len(listadegrupo)==0: #Si ya fueron evaluadas todas las palabras 
            listadegrupo.clear()
        listaY.append(1)
        
        return bocina.Speak(wordRandom) #Mencionar palabra aleatoria mostrada con voz

       
    #Boton para continuar con la siguiente palabra
    subboton=Button(ventananueva,text="Next word.",command=ponerpalabra, borderwidth=4)
    subboton.place(x=250,y=10)
    subboton.config(font=(letra, 20, "bold"), bg=rojo, fg="white")
    

    def reset(): #Funcion para reinciar ventana y preguntar nuevamente
        listadegrupo.clear()
        ventananueva.destroy()
        evaluargrupo()
    
    botonreset = Button(ventananueva, text="Reset", font=(letra, 20, "bold"), bg=rojo, fg="white", command=reset, borderwidth=4)
    botonreset.config(padx=35)

    botonreset.place(x=250, y=380)
        
        
#Boton para mostrar las palabras de los grupos en el cuadro rojo
boton_mostrar = Button(miframe, text="Evaluar",command=evaluargrupo)
boton_mostrar.place(x=355, y=206)
boton_mostrar.config(font=(letra, 12, "bold"), bg=rojo, fg="white")


#EDICION 
borde1 = tkinter.PhotoImage(file="borde1.png")
bordeuno = Label(miframe, image=borde1).place(x=0, y=242)
bordedos = Label(miframe, image=borde1).place(x=0, y=190)
bordetres = Label(miframe, image=borde1).place(x=0, y=637)
bordetres = Label(miframe, image=borde1).place(x=0, y=23)



img_usa=tkinter.PhotoImage(file="usa.png")
usa = Label(miframe, image=img_usa,bg=rojo).place(x=300, y=38)


flecha1=tkinter.PhotoImage(file="flecha.jpg")
flechauno = Label(miframe, image=flecha1, bg=azul).place(x=165, y=207)


def agregar_palabra(): #Agregar palabra a grupo digitado

    palabra_digitada = entrada_palabra.get()
    grupo_digitado = entry_grupo.get()
    insertar = f"INSERT INTO {grupo_digitado} VALUES('{palabra_digitada}')" #La query
    agregar = micursor.execute(insertar)
    miconexion.commit()
    entrada_palabra.delete(0, 'end')

#Entrada digitar la palabra que queremos agregar
entrada_palabra = Entry(miframe, bg="white", fg=azul, font=16)
entrada_palabra.focus() #Para que al entrar directamente se pueda escribir
entrada_palabra.place(x=113, y=60)

#Boton para agregar palabra a el grupo digitado
boton_agregar = Button(miframe, text="Agregar Palabra",bg=azul, command=agregar_palabra,takefocus=False)
boton_agregar.place(x=140, y=135)
boton_agregar.config(font=(letra, 11,"bold"), fg="white")


#----------- evaluar todos las palabras de todos los grupos ---------

listadetodos=[]
listaallwords=[]

consultatodos = f"SELECT name FROM sqlite_master WHERE type = 'table';"
alltables=micursor.execute(consultatodos)

for x in alltables:
    xstr=str(x)
    lean = xstr.replace("'", "")
    leanA = lean.replace("(", "")
    leanB = leanA.replace(")", "")
    leanC = leanB.replace(",", "")
    listadetodos.append(leanC)
    
    
for x in listadetodos:
    consulargrupos = f"SELECT * from {x}"
    tablasconsulas = micursor.execute(consulargrupos)
    for x in tablasconsulas:
        listaallwords.append(x)

#Mostrar cantidad de palabras en total
cantidadwords=Label(miframe,text=len(listaallwords))
cantidadwords.config(font=(letra, 20, "bold"), bg=rojo, fg="white")
cantidadwords.place(x=20,y=204)
evaluartodolista=[]

def evaluar_todo(): #Funcion para no sólo evaluar un grupo, si no todos los grupos creados
    for x in listaallwords:
        xstr = str(x)
        lean = xstr.replace("'", "")
        leanA = lean.replace("(", "")
        leanB = leanA.replace(")", "")
        leanC = leanB.replace(",", "")
        evaluartodolista.append(leanC)
    
    ventananueva = Toplevel()
    ventananueva.geometry("440x660")
    ventananueva.config(background=azul)
    listaY = [1, 0]
    listaX = [1, 0]

    def evalue():
        
        uno = 1
        wordRandom = random.choice(evaluartodolista)
        posword = evaluartodolista.index(wordRandom)
        suma = sum(listaY)

        if suma == 11:
            listaY.clear()
            capa = Label(ventananueva, bg=azul,
                        borderwidth=4)
            capa.config(pady=300, padx=120)
            capa.place(x=0, y=0)
        palabras = Label(ventananueva, text=f"{wordRandom}")
        evaluartodolista.pop(posword)
        palabras.config(font=(letra, 20), padx=5, background="white",
                        borderwidth=4, relief="raised", fg=azul)
        palabras.grid(row=suma, column=1)
        
        if len(evaluartodolista) == 0:
            evaluartodolista.clear()
        listaY.append(1)
        return bocina.Speak(wordRandom)

    subboton = Button(ventananueva, text="Next word.",
                      command=evalue, borderwidth=4)
    subboton.place(x=250, y=10)
    subboton.config(font=(letra, 20, "bold"), bg=rojo, fg="white")

    def reset():
        evaluartodolista.clear()
        ventananueva.destroy()
        evaluar_todo()

    botonreset = Button(ventananueva, text="Reset", font=(
        letra, 20, "bold"), bg=rojo, fg="white", command=reset, borderwidth=4)
    botonreset.config(padx=35)

    botonreset.place(x=250, y=380)
    
botontodo = Button(miframe, text="Evaluar todo",command=evaluar_todo)
botontodo.config(font=(letra, 12, "bold"), bg=rojo, fg="white")
botontodo.place(x=7, y=145)

root.mainloop()
