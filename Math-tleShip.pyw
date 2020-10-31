#Creado por Owen Jáuregui Borbón
#Matrícula: A01638122
#Creado el 22/10/2019

from tkinter import *
from tkinter import messagebox
from random import randint
from tkinter.ttk import Progressbar
import time, operator

#Celda dentro del tablero
class Celda(object):

	#Inicialización de la celda
	def __init__(self, canvas, cl, rw, maquina):
		self.pos        = [rw - 1, cl - 1]
		self.canvas     = canvas
		self.maquina    = maquina
		self.active     = True
		self.available  = True
		self.barco      = False
		self.canvas.grid(column = cl, row = rw)

		#Habilita la interacción con las celdas
		if maquina:
			self.canvas.bind("<Button-1>", self.atack)

	#Interaccion del usuario con las celdas de la máquina
	def atack(self, event):
		global tiros, barcosM
		widg = event.widget
		'''Revisa que el turno sea del usuario y que tenga tiros 
		suficientes para interactuar'''
		if turno == 2 and tiros > 0 and self.active:
			self.hit(barcosM, contadorM)

	'''Ataque a las casillas, tanto por parte de la máquina como del usuario,
	detección de barcos restantes y reductor de tiros restantes'''
	def hit(self, barcos, contador):
		global tiros, turno
		pos = self.pos
		if self.barco:
			self.canvas.config(bg = "#7800FF")
			for barco in range(len(barcos)):
				if pos in barcos[barco]:
					break
			barcos[barco].remove(pos)
			if barcos[barco] == []:
				barcos.pop(barco)
				contador.config(text = "Barcos: " + str(len(barcos)))
				if barcos == []:
					end(barcos)
					tiros = 1
		else:
			self.canvas.config(bg = "#00FCFF")
		self.active = False
		tiros -= 1
		if tiros == 0:
			if turno == 2:
				turno = 3
			elif turno == 3:
				turno = 1
			cambio()

	#Restauración de la celda
	def reset(self):
		self.active     = True
		self.available  = True
		self.barco      = False
		self.canvas.config(bg = "white")

#Creación de un tablero de batalla naval
def tablero(tab, x_, y_, interact = False):

	#Crea el marco del tablero
	frame = Frame(root, bg = "#DDDDDD")
	frame.place(x = x_, y = y_)

	etiqueta = Label(root, text = "Máquina" if interact else "Usuario", 
		             font = ("Arial", 14), bg = "#FFEBD9")
	etiqueta.place(x = x_ + (205 if interact else 0), y = y_ - 30)

	#Colocación de números para los ejes del tablero
	for columna in range(1, 11):
		coor = Label(frame, text = str(columna), bg = "#DDDDDD", width = 2, 
			         font = ("Times New Roman", 14), bd  = 1, relief = GROOVE)
		coor.grid(column = columna, row = 0)
	for fila in range(1, 11):
		coor = Label(frame, text = str(fila), bg = "#DDDDDD", width = 2, 
			         font = ("Times New Roman", 14), bd  = 1, relief = GROOVE)
		coor.grid(column = 0, row = fila)

	#Creación y colocación de cada celda del tablero en una matriz
	for fila in range(10):
		tab.append([])
		for columna in range(10):
			celda_ = Canvas(frame, width = 20, height = 20, bg = "white", 
				            bd = 1, relief = RAISED)
			celda  = Celda(celda_, columna + 1, fila + 1, interact)
			tab[fila].append(celda)

#Creación y posicionamiento de los barcos dentro del tablero
def barcos(tab, barcos):
	global contadorM, contadorJ
	'''Creación de las posiciones de los barcos con una separación 
	   de mínimo 1 celda entre ellos'''
	for tamaño in [5, 4, 3, 3, 2]:
		listo  = False
		facing = [0,1] if bool(randint(0,1)) else [1,0]
		barco  = []
		while not listo:
			x, y  = randint(0, 9 - tamaño*facing[0]),\
			        randint(0, 9 - tamaño*facing[1])
			barco = [[y + j*facing[1],x + j*facing[0]] for j in range(tamaño)]
			for celda in barco:
				listo = True
				if tab[celda[0]][celda[1]].barco or not \
				   tab[celda[0]][celda[1]].available:
					listo = False
					break

		'''Guardado de las posiciones del barco y actualización de los datos 
		de las celdas ocupadas o indisponibles'''
		for celda in barco:

			#Muestra la posición de los barcos del usuario
			if not tab[celda[0]][celda[1]].maquina:
				tab[celda[0]][celda[1]].canvas.config(bg = "#5E5E5E")

			'''Configura cuales celdas tinen, o no, barco y cuales no pueden 
			elegirse para el siguiente barco'''
			tab[celda[0]][celda[1]].barco = True
			rango_x = [-1*min(1, celda[1]), 1*min(1, 9 - celda[1])]
			rango_y = [-1*min(1, celda[0]), 1*min(1, 9 - celda[0])]
			for fila in range(rango_y[0], rango_y[1] + 1):
				for columna in range(rango_x[0], rango_x[1] + 1):
					tab[celda[0] + fila][celda[1] + columna].available = False
		barcos.append(barco)
    #Creación y colocación de marcadores de barcos restantes de los tableros
	if barcos == barcosM:
		contadorM = Label(root, text = "Barcos: " + str(len(barcos)), 
			              font = ("Arial", 10), bg = "#FFEBD9")
		contadorM.place(x = 465, y = 505)
	else:
		contadorJ = Label(root, text = "Barcos: " + str(len(barcos)), 
			              font = ("Arial", 10), bg = "#FFEBD9")
		contadorJ.place(x = 50, y = 505)

#Apertura de una ventana para la visualización las instrucciones
def ayuda():
	inst = Toplevel(root)
	inst.title("¿Cómo jugar?")
	try:
		inst.iconbitmap("Math-tleShip.ico")
	except:
		pass
	Label(inst, text = INSTRUCCIONES, justify = "left").pack()
						
'''Inicia el juego llamando a funciones para la creación de tableros y
posicionamiento de barcos. Remueve los widgets del menú y coloca los del
juego principal en pantalla'''
def start():
	global jugador, maquina
	tablero(jugador, 50, 220)
	tablero(maquina, 465, 220, interact = True)
	barcos(jugador, barcosJ)
	barcos(maquina, barcosM)
	pregunta.pack(side = LEFT)
	respuesta.pack(side = LEFT)
	responder.pack(side = LEFT)
	sub.place(x = 400, y = 50, anchor = N)
	subt.place(x = 400, y = 90, anchor = N)
	pausa.place(x = 400, y = 450, anchor = N)
	titulo.place_forget()
	titulo_.place_forget()
	listo.place_forget()
	ayuda.place_forget()
	cambio()
	juego()

'''Finalización de la partida, estipulación del ganador y colocación de los 
botones de reinicio y cierre del juego'''
def end(barcos):
	global turno
	if barcos == barcosJ:
		subts[0] = "Has Perdido, ¡Suerte Para la Próxima!"
	else:
		subts[0] = "¡Felicidades, Tú Ganas!"
	subt.config(font = ("Arial", 17))
	reiniciar.place(anchor = N, x = 400, y = 300)
	cerrar.place(anchor = N, x = 400, y = 350)
	turno = 0

'''Cierre del juego con verificación de seguridad en caso de dar click en el 
botón por accidente'''
def close():
	sure = messagebox.askyesno(title = "Salir del juego", icon = "warning", 
		   message = "¿Está seguro de querer salir?")
	if sure:
		root.destroy()

#Activación y desactivación de la pausa mediante el botón "pausa"
def pausa():
	global pause
	pause = not pause

#Reinicio del juego al terminar una partida, activado por el botón "reiniciar"
def restart():
	global barcosJ, barcosM, turno
	barcosJ, barcosM = [], []
	#Restauración de todas las celdas a sus valores originales
	for fila in jugador:
		for celda in fila:
			celda.reset()
	for fila in maquina:
		for celda in fila:
			celda.reset()
	barcos(jugador, barcosJ)
	barcos(maquina, barcosM)
	reiniciar.place_forget()
	cerrar.place_forget()
	turno = 1
	cambio()

'''Genera una nueva pregunta dependiendo de la dificultad y calcula el 
resultado para guardarlo como la respuesta correcta'''
def nuevaPreg():
	global ECUACIONES, OPERADORES, DIVISIONES, preg
	'''Ajuste del tiempo del temporizador dependiendo de la dificultad y el 
	número de tiros que adquiriera el usuario'''
	temp["maximum"] = 100 + (dific-1)*30 - tiros*15
	temp["value"] = temp["maximum"]

	first      = True
	preg[0]    = ""
	respuesta  = 0
	#Selección de la plantilla para la pregunta dependiendo de la dificultad
	pregun     = ECUACIONES[dific - 1][randint(0,1)]
	operations = pregun.replace("(", "").replace(")", "").split(" ")
	'''Traducción de caracteres a operadores y operandos para el cálculo de 
	la respuesta'''
	for i in range(1, len(operations), 2):
		'''Selección aleatoria entre pares de operadores dependiendo del 
		caracter de la plantilla'''
		operator = operations[i]
		if operator == ":":
			operator = "÷" if bool(randint(0, 1)) else "x"
		elif operator == "#":
			operator = "+" if bool(randint(0, 1)) else "-"
		operations[i] = operator
		'''Selección aleatoria de operandos dependiendo de la dificultad
		En caso de ser división, se selecciona un par de números de la 
		lista de divisiones enteras. Los operandos se ordenan dentro de una 
		lista para después realizar el cálculo del resultado'''
		if first and operator == "÷":
			operations[i-1], operations[i+1] = DIVISIONES[randint(dific - 1, 
														  dific*3 - 1)]
			respuesta = operations[i-1]
			first = False
		elif first:
			respuesta = randint(1 + dific, 4 + dific)
			operations[i-1] = respuesta
			operations[i+1] = randint(1 + dific, 3 + dific)
			first = False
		else:
			operations[i+1] = randint(1 + dific, 3 + dific)
		respuesta = OPERADORES[operator](respuesta, operations[i+1])
	#Realización secuencial del cálculo con los operadores y operandos elegidos
	for car in pregun:
		if car not in " ()":
			preg[0] += str(operations.pop(0))
		else:
			preg[0] += car
	preg[1] = int(respuesta)
	'''Recolocación de el widget de entrada y la pregunta dependiendo de la 
	longitud de la operación'''
	pregunta.config(text = preg[0] + " = ")
	frameResp.place(x = 335 - len(preg[0])*5.2, y = 150)

'''Recibe la respuesta del widget "Respuesta" y comprueba si es, o no, 
correcta. Esta función solo se activa mediante el botón "Responder" '''
def contestar():
	global tiros, turno, dific
	resp_ = resp.get()
	#Comprobación de que el dato ingresado es un número
	try:
		int(resp_)
	except ValueError:
		'''Comprobación de que el número sea un entero. Al no haber
		respuestas decimales, si se ingresa un decimal se tomará como 
		incorrecta'''
		try:
			float(resp_)
		except ValueError:
			pass
		else:
			turno  = 2
			cambio()
	else:
		'''Comprobación de que la respuesta sea correcta y modificación de 
		dificultad dependiendo de la cantidad de respuestas correctas'''
		if int(resp_) == preg[1]:
			if tiros < 4:
				tiros += 1
				nuevaPreg()
			elif tiros == 4:
				tiros += 1
				turno  = 2
				dific += int(dific < 4)
				cambio()
			respuesta.config(bg = "#64FF64")
		else:
			if tiros < 3:
				dific -= int(dific > 1)
			turno  = 2
			respuesta.config(bg = "#FF4343")
			root.after(300,cambio)
	resp.set("")


'''Ataque de la máquina al tablero del jugador, con una precisión que depende 
de la dificultad'''
def ai():
	global tiempo
	if tiempo % 15 == 14:
		prob_rand = 7 - dific #Probabilidad de disparo aleatorio en base a 10
		if randint(1, 10) >= prob_rand:
			'''Selección de una celda para atacar en un rango desde alguna 
			celda que contenga un barco. El rango depende de la dificultad'''
			barco     = barcosJ[randint(0, len(barcosJ) - 1)]
			objetivo  = barco[randint(0, len(barco) - 1)]
			prec = 4 - (dific - int(dific > 1))
			opciones = []
			for j in range(objetivo[0] - prec, objetivo[0] + prec):
				for i in range(objetivo[1] - prec, objetivo[1] + prec):
					'''Chequeo para que las celdas seleccionadas sí existan 
					dentro del tablero'''
					if (j >= 0 and i >= 0) and (j < 10 and i < 10):
						#Chequeo para saber si la celda ya ha sido atacada
						if jugador[j][i].active:
							opciones.append(jugador[j][i])
			opciones[randint(0, len(opciones) - 1)].hit(barcosJ, contadorJ)
		else:
			'''Selección de una celda aleatoria del tablero que no haya sido 
			atacada con anterioridad'''
			objetivo = jugador[randint(0,9)][randint(0,9)]
			while not objetivo.active:
				objetivo = jugador[randint(0,9)][randint(0,9)]
			objetivo.hit(barcosJ, contadorJ)
	tiempo += 1

#Contador de tiempo y actualización dentro del temporizador
def crono():
	global turno
	temp["value"] -= 1
	#En caso de que el temporizador llegue a 0, se pasa al siguiente turno
	if temp["value"] <= 0:
		turno = 2
		cambio()


'''Función para la activación y desactivación de widgets para cada turno 
cuando este cambia'''
def cambio():
	global tiros, turno, dific
	'''Colocación de el widget de entrada de datos, temporizador, problema y 
	desactivación del botón de pausa'''
	if turno == 1:
		shots.place(x = 0, y = 20)
		frameResp.place(x = 335 - len(preg[0])*5.2, y = 150)
		temp.place(x = 0, y = 0)
		pausa.config(state = DISABLED)
		nuevaPreg()
	#Remueve los widgets colocados en el turno 1 y los reestablece
	elif turno == 2:
		shots.place(x = 0, y = 0)
		respuesta.config(bg = "white")
		resp.set("")
		frameResp.place_forget()
		temp.place_forget()
		#Configuración del cursor con forma de "objetivo" sobre las celdas
		for fila in maquina:
			for cuadro in fila:
				cuadro.canvas.config(cursor = "target")
		'''En caso de que el jugador no lograra obtener ningún tiro, se pasa 
		al siguiente turno de forma automática'''
		if tiros == 0:
			turno = 3
			dific -= int(dific > 1)
			cambio()
	#Activación del botón de pausa y restauración de el cursor sobre las celdas
	elif turno == 3:
		for fila in maquina:
			for cuadro in fila:
				cuadro.canvas.config(cursor = "arrow")
		tiempo = 0
		tiros  = 5
		pausa.config(state = ACTIVE)
	#Actualización de los subtítulos correspondientes al turno
	sub.config(text = subs[turno])
	subt.config(text = subts[turno])

#Código de ejecución ciclica para la repetición de los turnos
def juego():
	#Efecto de pausa del juego
	if not pause:
	#Ejecución de secciones del programa dependiendo del turno
		if turno == 1:
			crono()
		if turno == 3:
			ai()
		shots.config(text = "Tiros Disponibles: " + str(tiros))
	root.after(100, juego)

'''Ecuaciones para preguntas del juego, operadores para traducción
   dentro de las ecuaciones y pares de divisiones para evitar decimales'''
ECUACIONES = [["X # X", "X : X"],
			  ["X # X # X", "X : X # X"],
			  ["(X : X) x X", "(X : X) x X # X"],
			  ["(X : X # X) x X", "(X : X # X) x X # X"]]
OPERADORES = {"+" : operator.add, "-" : operator.sub, "x" : operator.mul, 
			  "÷" : operator.truediv}
DIVISIONES = [[4, 2], [12, 6], [12, 3], [15, 5], [18, 2], [18, 3], [24,4],
             [21, 7], [36, 9], [56, 8], [63, 9], [81, 9]]

#Instrucciones de juego
INSTRUCCIONES = '''
En este juego tu mejor aliado sera la lógica, y el tiempo será tu peor enemigo.

Dentro del juego hay 3 etapas:
	1. Resolución de problemas.
	2. Ataque a las casillas del enemigo.
	3. Ataque enemigo.

1. Resolución de problemas:
	En esta etapa tendrás que responder correctamente a los cálculos que se
	te pida realizar. Cuándo tengas la respuesta correcta, da click en el
	botón de "OK" y verifica tu respuesta. Cada respuesta correcta será un
	tiro que podrás usar en el siguiente turno. Pero cuidado, no lo pienses de
	más, pues hay un temporizador que se volverá más rápido conforme contestes
	las preguntas. Además, toma en cuenta que el juego se adapta, mientras
	mejor contestes las preguntas y más tiros consigas, las preguntas serán
	más dificiles.

2. Ataque a las casillas del enemigo:
	Ya obtuviste tiros, ahora debes usarlos. Para atacar las casillas del
	enemigo solo debes dar click sobre el punto exacto del tablero enemigo
	que quieres atacar. Si la casilla se marca de color azul, significa que
	fallaste el tiro, y tu munición quedó perdida en el mar. De lo contrario,
	si la casilla se marca de color morado, significa que acertaste y ahora
	uno de los barcos del enemigo está dañado. Para hundir uno de los barcos
	tines que acrtar a todas las casillas en las que este se encuntre. En la
	parte inferior podrás ver cuantos barcos restantes hay en el campo de 
	guerra.

3. Ataque enemigo
	Esta es la última etapa antes de iniciar nuevamente por la primera, el
	enemigo intentará hundir tus barcos. En este punto no puedes mas que 
	resignarte ante el destino y cruzar los dedos para que el enemigo no
	explote la proa de alguno de tus barcos. Con 5 explosiones dirigidas a tu
	territorio, el enemigo intenta localizar tus barcos, mas no sabe con
	exactitud dónde se encuentran. Al igual que las preguntas, mientras mejor
	seas en el juego, más inteligentes y precisos serán los ataques enemigos.

¿Cómo se gana? muy simple, hunde al enemigo. Si logras hundir todos sus barcos
ganarás. Pero recuerda, si el hunde tus barcos primero... bueno... será mejor
que consigas un bote salvavidas. Suerte, y recuerda, responde con lógica, se
rápido y preciso antes de que el enemigo lo sea
'''

#Ventana principal del juego, advertencia de cierre de ventana, ícono y título
root = Tk()
root.config(bg = "#FFEBD9")
root.geometry("800x550")
root.title("Math-tle Ship")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", close)
try:
	root.iconbitmap("Math-tleShip.ico")
except:
	pass

'''Reguladores de etapas de juego, respuesta, tableros y tecto de los 
subtitulos de etapa'''
turno   = 1
dific   = 1
tiros   = 0
tiempo  = 0
pause   = False
subs    = ["SE ACABÓ EL JUEGO",
		   "TU TURNO",
		   "TU TURNO",
		   "TURNO DE LA MÁQUINA"]
subts   = ["",
		   "Contesta las Operaciones",
		   "Ataca a los Barcos de la Máquina",
		   "Preparate para Tu Siguiente Turno",]
preg    = ["", 0]
resp    = StringVar()
barcosJ, barcosM = [], []
jugador, maquina = [], []

#Título de la pantalla de inicio de juego
titulo  = Canvas(root, bg = "#FFEBD9")
titulo1 = Label(titulo, text = "M", bg = "#FFEBD9", bd = 0, fg = "#8400AF", 
	              font = ("Rockwell", 80))
titulo2 = Label(titulo, text = "ath-tle", bg = "#FFEBD9", bd = 0, 
	              font = ("Rockwell", 80))
titulo_ = Canvas(root, bg = "#FFEBD9")
titulo3 = Label(titulo_, text = "S", bg = "#FFEBD9", bd = 0, fg = "#00CCFF", 
	              font = ("Rockwell", 80))
titulo4 = Label(titulo_, text = "hip", bg = "#FFEBD9", bd = 0, 
	              font = ("Rockwell", 80))
titulo1.pack(side = LEFT)
titulo2.pack(side = LEFT)
titulo3.pack(side = LEFT)
titulo4.pack(side = LEFT)
titulo.place(x = 400, y = 50, anchor = N)
titulo_.place(x = 400, y = 150, anchor = N)

'''Creación de botones para el inicio del juego y para la visualización de 
instrucciones'''
listo     = Button(root, text = "Empezar Juego", font = ("Arial", 20), 
	               activebackground = "#D46AFC", bg = "#8400AF", fg = "white", 
	               cursor = "hand2", command = start)
ayuda     = Button(root, text = "Instrucciones", font = ("Arial", 18), 
	               activebackground = "#CEFDFF", bg = "#00CCFF", fg = "white", 
	               cursor = "hand2", command = ayuda)
listo.place(x = 400, y = 340, anchor = N)
ayuda.place(x = 400, y = 430, anchor = N)


'''Botones de reinicio y cierre del juego al finalizar una partida'''
reiniciar = Button(root, text = "REINICIAR", bg = "#5D6564", fg = "white", 
	               font = ("Arial", 12), activebackground = "#8FFFB4", 
	               cursor = "exchange", command = restart)
cerrar    = Button(root, text = "SALIR", bg = "#5D6564", fg = "white", 
	               font = ("Arial", 12), activebackground = "#A31616", 
	               cursor = "hand2", command = close)

'''Boton de pausa, presentación de subtítulos de etapa de juego y tiros 
disponibles para cada etapa'''
pausa     = Button(root, text = "PAUSA", font = ("Arial", 12), cursor = \
	               "hand2", command = pausa)
sub       = Label(root, text = subs[turno], bg = "#FFEBD9", font = \
	              ("Elephant", 20))
subt      = Label(root, text = subts[turno], bg = "#FFEBD9", font = \
	              ("Arial", 11))
shots     = Label(root, text = "Tiros Disponibles: " + str(tiros), 
	              bg = "#FFEBD9", font = ("Arial", 10))

'''Creación del marco para mostrar y responder los cálculos, y temporizador 
para la contestación de la pregunta'''
frameResp = Frame(root, bg = "#FFEBD9")
pregunta  = Label(frameResp, text = preg[0] + " = ", bg = "#FFEBD9", font = 26)
respuesta = Entry(frameResp, textvariable = resp, bg = "white", font = 26, 
	              width = 7, justify = CENTER)
responder = Button(frameResp, text = "OK", activebackground = "white", 
	               padx = 7, cursor = "hand2", command = contestar)
temp      = Progressbar(root, orient = HORIZONTAL, length = 800)

#Ciclo principal de Tkinter
root.mainloop()