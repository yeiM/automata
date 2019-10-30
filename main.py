import pyttsx3
from tkinter import *
from pila import Pila 
from pushDownAutomaton import PDA
import speech_recognition as sr
import time
import unidecode

label_PtoP = ["p-p","b/b/bb", "a/b/ba", "b/a/ab", "a/a/aa", "b/#/#b", "a/#/#a"]
label_PtoQ = ["p-q","c/#/#", "c/b/b", "c/a/a"]
label_QtoQ = ["q-q","b/b/λ", "a/a/λ"]
label_QtoR = ["q-r","λ/#/#"]

edges1 = [label_PtoQ, label_PtoP, label_QtoR, label_QtoQ]


def funtion(boton):
    #print("click")
    
    if boton == True:
        botonRapido.config(bg="#a528ec")
        botonLento.config(bg="#a528ec")
        botonRapido.select()
        pila.sapi = False
        
    else:
        botonRapido.config(bg="#a528ec")
        botonLento.config(bg="#a528ec")
        botonLento.select()
        pila.sapi = True


def cambiarImagen(elegir, automata):
    
    photo2 = PhotoImage(file="resources/"+automata+elegir+".png")
    label1.configure(image=photo2)
    label1.image = photo2

def comenzar():

    if txtUsuario.get() != "":
        resultado = automata1.evaluarCadena(txtUsuario.get(), automata1.estadoInicial, automata1.pila, automata1.proceso)
        pila.dibujarPila()

        cadena = ""
        if resultado == True:
            cadena = "Cadena Aceptada"
        else:
            cadena = "Cadena no Aceptada"

        if pila.indiceDeTexto != -1:
            canvas2.delete(pila.indiceDeTexto)
            pila.indiceDeTexto = -1

        pila.indiceDeTexto = canvas2.create_text(140, 20, text=cadena , activefill="blue", font="ArialBlack")

    else:
        hablar("Por favor, introduzca una cadena de caracteres")
    
def hablar(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.languages[0] == u'es-la':
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 130)
    engine.say(message)
    engine.runAndWait()

def fasd():
    print("Speak: ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            x = r.recognize_google(audio, language='es-la')
            if x.lower() == 'lento':
                funtion(False)
                fasd()
            elif x.lower() == 'rápido' or x.lower() == 'rapido':
                funtion(True)
                fasd()
            elif x.lower() == 'comenzar':
                comenzar()
            elif x.lower() == 'palabras' or x.lower() == 'palabra':
                hablar("Por favor, diga la palabra a evaluar")
                audio2 = r.listen(source)
                audioPalabra = r.recognize_google(audio2, language='es-la')
                audioPalabra = unidecode.unidecode(audioPalabra)
                txtUsuario.insert(0, audioPalabra)
                fasd()

        except sr.UnknownValueError:
            hablar('No te pude entender')
            fasd()
        except sr.RequestError as e:
            print("Cannot obtain results; {0}".format(e))

class pilaGrafica:
    def __init__(self, coord, proceso, canvas):
        self.coord = coord
        self.lista = []
        self.mensajes = []
        self.proceso = proceso
        self.canvas = canvas
        self.mensaje = ""
        self.bandera = 0
        self.automata = "Palindromo Impar"   
        self.indiceDeTexto = -1
        self.sapi = True


    def aumentarPila(self):
        
        if len(self.lista) < 10:
            #i, m = pintarPila(self.coord, mensaje)
            i = self.canvas.create_rectangle(self.coord, width=1, fill='#8245a0', activefill="#0017F9")
            m = self.canvas.create_text(self.coord[2]-90, self.coord[1]+20, text = self.mensaje, activefill="blue")

            self.lista.append(i)
            self.mensajes.append(m)
            self.coord = self.coord[0], self.coord[1]-50, self.coord[2], self.coord[3]-50

    def decrementarPila(self):

        self.coord = self.coord[0], self.coord[1]+50, self.coord[2], self.coord[3]+50
        self.canvas.delete(self.lista.pop())
        self.canvas.delete(self.mensajes.pop())
        #borrarPila(self.lista.pop(), self.mensajes.pop())

    def dibujarPila(self):

        if self.bandera < len(self.proceso):
            
            w = self.proceso[self.bandera]

            destino = None
            ver = w[3]
    
            #Divido el string para saber Nodo origen a nodo destino
            if len(ver) > 1:
                divido = ver.split("-")
                destino = divido[1]

            if w[1] == 1:
                self.mensaje = w[0]
                self.aumentarPila()
                
                if pila.sapi == True:
                    hablar("Introduzco el item " + w[0] + " en la pila")
                
                cambiarImagen(w[3], self.automata)
        
            else:
                self.decrementarPila()
                
                if pila.sapi == True:
                    hablar("Saco el item " + w[0] +" de la pila")
                
                cambiarImagen(w[3], self.automata)
            
            if destino != None:
                self.canvas.after(800, lambda:cambiarImagen(destino, self.automata))
            
            if pila.indiceDeTexto != -1:
                canvas2.delete(pila.indiceDeTexto)
                pila.indiceDeTexto = -1
            
            pila.indiceDeTexto = canvas2.create_text(170, 20, text = w[2], activefill="blue", font="ArialBlack")
            
            self.bandera += 1
            self.canvas.after(1000, self.dibujarPila)


coord = 70, 430, 250, 480

main_window = Tk()
main_window.title("Automata Impar")
main_window.geometry("720x675")
main_window.resizable(0,0)

main_window.config(background= 'white')
main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(0, weight=1)

imagenAuto = PhotoImage(file="resources/Palindromo Impar.png")

#Espacio de la imagen 
label1 = Label(main_window, bg='#fbbccc', image=imagenAuto, width=580, height=350,borderwidth=0)
label1.grid(row=1, column=0, sticky="nsew")

#espacio pila 
label2 = Label(main_window, bg='black', width=150, height=50,borderwidth=0)
label2.grid(row=1, column=1, sticky="nsew")

#espacio de estados 
label4 = Label(main_window, text="Estado", bg='black',borderwidth=0)
label4.place(x=425,y=0)

#cuadro donde se ingresa el estado 
canvas2 = Canvas(label4, bg='#fbbccc', width=295, height=53)
canvas2.grid(row=1,column=0)

#cuadro donde se ingresa la pila
canvas = Canvas(label2, bg='#fbbccc', width=449, height=100)
canvas.pack(expand=YES, fill=BOTH)

#cuadro donde se ingresa palabra 
label3 = Label(main_window, bg='#fbbccc',borderwidth=0)
label3.grid(row=0, column=0, sticky="nsew")


entrada = StringVar()

txtUsuario = Entry(label3, textvariable=entrada )
txtUsuario.pack()

automata1 = PDA("p", "r", "#")
automata1.setEdges(edges1)

pila = pilaGrafica(coord, automata1.proceso, canvas)

comenzarProceso = Button(label3, text="Comenzar", command=comenzar, bg='#bd52e3')
comenzarProceso.pack(expand=False, fill=BOTH)

botonLento = Radiobutton( text="Lento",  bg='#bd52e3',width=10, command=lambda:funtion(False), value = "1")
botonLento.place(x=90,y=100)
botonRapido = Radiobutton( text="Rapido", bg='#bd52e3',width=10, command=lambda:funtion(True), value = "2")
botonRapido.place(x=195,y=100)

boton_escuchar = Button(label3, text="grabar", bg="#bd52e3", command=lambda:fasd()) #LLAMAMOS PARA RECONOCER LA VOZ
boton_escuchar.pack(expand=False, fill=BOTH)

main_window.rowconfigure(1, weight=200)

main_window.columnconfigure(1, weight=1)
main_window.columnconfigure(3, weight=1)

main_window.mainloop()

            