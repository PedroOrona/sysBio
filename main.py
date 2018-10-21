# coding=UTF-8
"""
@author: Pedro Augusto
UFMS - Universidade Federal de Mato Grosso do Sul
"""
from tkinter import *
from tkinter.ttk import *
from bluetooth import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import pyplot
from matplotlib import animation
from numpy import random, sin, exp
from pprint import pprint
from multiprocessing import Process, Queue, Pipe
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog
from struct import *
import numpy as np
import string
import sys
import pylab
import os
import glob
import serialRead
import bluetoothRead
import serial
import plotter
import time
import csv

vertical_scale = 4200
horizontal_scale = 20
mygreen = "#698B22"
mygreen2 = "#9ACD32"

def abrir(): print("abrir")
def salvar(): app.save_figure()
def ajuda() : print("ajuda")
def sair(): root.quit()

def set_vertical_gain_5(): app.vertical_gain(5)
def set_vertical_gain_10(): app.vertical_gain(10)
def set_vertical_gain_20(): app.vertical_gain(20)   
def set_vertical_gain_40(): app.vertical_gain(40)  
def set_vertical_gain_80(): app.vertical_gain(80)  

def set_horizontal_gain_12(): app.horizontal_gain(12.5)
def set_horizontal_gain_25(): app.horizontal_gain(25)
def set_horizontal_gain_50(): app.horizontal_gain(50)

def record():
	win = Toplevel()
	win.title("Ficha do Paciente")
	win.geometry("520x600")

	fields = 'Identificador do Paciente', 'Fumante', 'Alcoolismo', 'Abuso de Drogas', 'Medicação',' Peso[kg]', 'Altura[cm]', 'Gênero', 'Tendência', 'Problema de Visão', 'Problema Cardíaco', 'Data de Nascimento', 'Classificação do Paciente (ICD)', 'Tamanho da Cabeça (mm)', 'Posição do Eletrodo de Referência', 'Posição do Eletrodo Terra'
	values = ('Sim', 'Não', 'Desconhecido')
	gender = ('Masculino', 'Feminino', 'Não especificado')
	hand = ('Destro', 'Canhoto', 'Ambos', 'Desconhecido')
	entries = []

	for field in fields:
		frameP = Frame(win)
		lab = Label(frameP, width=35, text=field, anchor='w')
		frameP.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)

		if field == 'Fumante':
			cb_valor1 = Combobox(frameP, values=values, state='readonly')
			cb_valor1.current(2)  
			cb_valor1.pack(side=RIGHT, expand=YES, fill=X)

		elif field == 'Alcoolismo':
			cb_valor2 = Combobox(frameP, values=values, state='readonly')
			cb_valor2.current(2)  
			cb_valor2.pack(side=RIGHT, expand=YES, fill=X)

		elif field == 'Abuso de Drogas':
			cb_valor3 = Combobox(frameP, values=values, state='readonly')
			cb_valor3.current(2)  
			cb_valor3.pack(side=RIGHT, expand=YES, fill=X)
		
		elif field == 'Medicação':
			cb_valor4 = Combobox(frameP, values=values, state='readonly')
			cb_valor4.current(2)  
			cb_valor4.pack(side=RIGHT, expand=YES, fill=X)

		elif field == 'Gênero':
			cb_valor5 = Combobox(frameP, values=gender, state='readonly')
			cb_valor5.current(2) 
			cb_valor5.pack(side=RIGHT, expand=YES, fill=X)

		elif field == 'Tendência':
			cb_valor6 = Combobox(frameP, values=hand, state='readonly')
			cb_valor6.current(3)  
			cb_valor6.pack(side=RIGHT, expand=YES, fill=X)

		elif field == 'Problema de Visão':
			vision = ('Sim', 'Não', 'Desconhecido', 'Sim, mas corrigido')
			cb_valor7 = Combobox(frameP, values=vision, state='readonly')
			cb_valor7.current(2)  
			cb_valor7.pack(side=RIGHT, expand=YES, fill=X)
		
		elif field == 'Problema Cardíaco':
			card = ('Sim', 'Não', 'Desconhecido', 'Marcapasso Cardíaco')
			cb_valor8 = Combobox(frameP, values=card, state='readonly')
			cb_valor8.current(2)  
			cb_valor8.pack(side=RIGHT, expand=YES, fill=X)			 

		else:
			ent = Entry(frameP)
			if field == 'Data de Nascimento':
				ent.insert(0, '21/10/1993')
			elif field == 'Posição do Eletrodo de Referência':	
				ent.insert(0, 'x,y,z')
			elif field == 'Posição do Eletrodo Terra':
				ent.insert(0, 'x,y,z')
			ent.pack(side=RIGHT, expand=YES, fill=X)
			entries.append((field, ent))

	#define os botões
	Button(win, text="Salvar", command= lambda: app.gdfConstruct(win, entries, cb_valor1, cb_valor2, cb_valor3, cb_valor4, cb_valor5, cb_valor6, cb_valor7, cb_valor8)).pack(fill="none", expand=True, side = LEFT)
	Button(win, text="Cancelar", command= lambda: win.destroy()).pack(fill="none", expand=True, side = LEFT)  

def module_preferences():
	#cria uma nova janela
	win = Toplevel()
	win.title("Preferências do Módulo")
	win.geometry("400x220")

	fields = 'Constante de Conversão para Volts', 'Deslocamento (Offset)', 'Ganho','Taxa de Transmissão', 'Taxa de Amostragem'
	entries = []

	for field in fields:
		frameP = Frame(win)	
		lab = Label(frameP, width=30, text=field, anchor='w')
		ent = Entry(frameP)
		frameP.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT, expand=YES, fill=X)
		entries.append((field, ent))

	#define os botões
	Button(win, text="Salvar", command= lambda: app.save_preferences(win, entries)).pack(fill="none", expand=True, side = LEFT)
	Button(win, text="Cancelar", command= lambda: win.destroy()).pack(fill="none", expand=True, side = LEFT)  

def conectarS(): 
	result = app.serial_ports()
	if len(result) == 0:
		tkMessageBox.showerror("Erro", "Nenhuma porta serial disponível")
		return

	#cria uma nova janela
	win = Toplevel()
	win.title("Serial")
	win.geometry("350x350")

	Panel = Frame(win)
	Panel.pack(side=TOP, fill=BOTH, expand=Y)

	cbp1 = Labelframe(Panel, text='Portas Disponíveis')
	cb_port = Combobox(cbp1, values=result, state='readonly')
	cb_port.current(0)  # set selection
	cb_port.pack(pady=5, padx=10)    

	paridades = ('Nenhuma', 'Par', 'Ímpar')

	cbp2 = Labelframe(Panel, text='Bit de Paridade')
	cb_parity = Combobox(cbp2, values=paridades, state='readonly')
	cb_parity.current(0)  # set selection
	cb_parity.pack(pady=5, padx=10)    

	state = ('Ativado', 'Desativado')

	cbp3 = Labelframe(Panel, text='RTS')
	cb_RTS = Combobox(cbp3, values=state, state='readonly')
	cb_RTS.current(1)  # set selection
	cb_RTS.pack(pady=5, padx=10) 

	cbp4 = Labelframe(Panel, text='DTR')
	cb_DTR = Combobox(cbp4, values=state, state='readonly')
	cb_DTR.current(1)  # set selection
	cb_DTR.pack(pady=5, padx=10)    

	cbp1.pack(in_=Panel, side=TOP, pady=5, padx=10)
	cbp2.pack(in_=Panel, side=TOP, pady=5, padx=10)
	cbp3.pack(in_=Panel, side=TOP, pady=5, padx=10)
	cbp4.pack(in_=Panel, side=TOP, pady=5, padx=10)

	Button(win, text="Conectar", command= lambda: app.connect_serial(cb_port, cb_parity, cb_RTS, cb_DTR, win)).pack(in_=Panel, side=BOTTOM, pady=5, padx=10)  

def conectarB(listNodes,win): 
	#fecha a janela dos dispositivos disponíveis com bluetooth
	dString = listNodes.get(listNodes.curselection())
	addr = dString.split("- ", 1)[1]
	win.destroy()
	app.connect_bluetooth(addr)

def dispositivos():
	#cria uma nova janela
	win = Toplevel()
	win.title("Bluetooth")
	win.geometry("320x320")

	Label(win, text="Dispositivos disponíveis").pack()

	frame = Frame(win)
	frame.pack()

	listNodes = Listbox(frame, width=25, height=10, font=("Helvetica", 12))
	listNodes.pack(side="left", fill="y")

	scrollbar = Scrollbar(frame, orient="vertical")
	scrollbar.config(command=listNodes.yview)
	scrollbar.pack(side="right", fill="y")

	listNodes.config(yscrollcommand=scrollbar.set)

	#cria o botão de conectar
	Button(win, text="Conectar", command= lambda: conectarB(listNodes,win)).pack(fill="none", expand=True, side = LEFT)
	#Button(win, text="Atualizar", command= lambda: ).pack(fill="none", expand=True, side = LEFT)
	
	#procura pelos dispositivos disponíveis
	nearby_devices = discover_devices(lookup_names = True)
	print("encontrou %d dispositivo(s)" % len(nearby_devices))

	if(len(nearby_devices) > 0):
		for name, addr in nearby_devices:
			listNodes.insert(END, "%s - %s" % (addr, name))

root=Tk()
root.style = Style()
root.style.theme_use("clam")

s = Style()
s.configure('TButton', background = mygreen, foreground='white', font = ('Kreativ', '9'), relief=FLAT, width = 8)
s.configure('TLabel')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
dpi = 96.0

# título da janela
root.wm_title("Gráfico em tempo real") 

class CustomToolbar(NavigationToolbar2TkAgg):
	def __init__(self,canvas_,parent_):

		directory = os.path.dirname(os.path.abspath(__file__))

		self.toolitems = (
			(None, None, None, None),
			('Home', 'Resetar para a visão original', 'home' , 'home'),
			('Back', 'Voltar para a visão anterior', directory + '/icons/icon_back_arrow', 'back'),
			('Forward', 'Ir para a próxima visão', directory + '/icons/icon_go_arrow', 'forward'),
			(None, None, None, None),
			('Pan', 'Eixos panorâmicos com botão esquerdo do mouse, zoom com o direito', directory + '/icons/move', 'pan'),
			('Zoom', 'Zoom Retangular', 'zoom_to_rect', 'zoom'),
			(None, None, None, None),)

		NavigationToolbar2TkAgg.__init__(self,canvas_,parent_)

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.parent = master
		self.top = Frame()
		self.top.grid()
		self.top.update_idletasks()
		self.vertical_limit = 0.0
		self.horizontal_limit_1 = 0.0
		self.horizontal_limit_0 = 0.0
		
		master.columnconfigure(0, weight=1)
		master.rowconfigure(0, weight=1)

		self.top.columnconfigure(0, weight=1)
		self.top.rowconfigure(0, weight=1)
		
		self.x = 0
		self.i = 0
		self.delta_i = 1
		self.update = 2
		# maximum number of points to acquire
		self.n_data = 10000     
		self.xy_data = []

		width = root.winfo_screenwidth() / dpi

		# figsize (w,h tuple in inches) dpi (dots per inch)
		self.figure = pyplot.figure(figsize=(width,12), dpi=dpi, facecolor='#DCDCDC')
		
		self.subplot = self.figure.add_subplot(211, axisbg='#DCDCDC')
		self.subplot.grid(True)

		# define amplitude dos eixos
		#self.subplot.axis([0, horizontal_scale, -vertical_scale, vertical_scale])
		self.ax = self.subplot.axis([0, horizontal_scale, 0, vertical_scale])
		self.subplot.set_xbound(lower=0, upper=None)

		pyplot.xlabel('s')
		pyplot.ylabel('mV')

		self.tupla = self.subplot.transData.transform([(0,1),(1,0)])-self.subplot.transData.transform((0,0))
		#print self.tupla
	 
		self.line, = self.subplot.plot([],[], animated=True) # initialize line to be drawn
		# Note: The comma after line is because the right hand size returns
		#   a one element list, and we want to unpack that single element
		#   into line, not assign the list to line.
		self.text = pyplot.figtext(0.05,0.25,"") # initialize text section

		self.canvas = FigureCanvasTkAgg(self.figure, master=root)
		self.canvas.get_tk_widget().configure(highlightcolor='#DCDCDC')
		self.canvas.get_tk_widget().grid(row=2,column=0,columnspan=3)
		self.background = self.canvas.copy_from_bbox(self.subplot.bbox)


		#Cria a barra de ferramentas
		toolbar_frame = Frame(self.parent)
		toolbar_frame.grid(row=1, pady= 31, sticky=W+N) 
		#toolbar_frame.grid(row=1, sticky=W+S) 
		toolbar = CustomToolbar(self.canvas,toolbar_frame)

		#toolbar.grid(row=0, column=1)

		toolbar_frame.columnconfigure(0, weight=1)
		toolbar_frame.rowconfigure(0, weight=1)

		self.button_text = ['Iniciar','Pausar', 'Parar']
		self.buttons = [None] * len(self.button_text)
		self.buttonframe = Frame(root)
		#self.buttonframe.columnconfigure(0, weight=10)  
		#self.buttonframe.rowconfigure(0, weight=30)  
		self.buttonframe.grid(row=1, sticky=N+W) 

		for button_index in range(len(self.button_text)):
			button_id = Button(self.buttonframe, text = self.button_text[button_index])
			#button_id.columnconfigure(button_index)
			button_id.grid(row=0, column=button_index)
			self.buttons[button_index] = button_id

			def button_handler(event, self=self, button=button_index):
				return self.service_buttons(button)

			button_id.bind("<Button-1>", button_handler)

		#variáveis de configuração do módulo
		self.constant = 1
		self.offset = 0
		self.gain = 1
		self.baud_rate = 115200
		self.sampling_rate = 240
		self.connect = 2

		self.GDFile = open("gdf_data_" + time.strftime("%H:%M") +".dat", "wb")
		self.flag_file = 0
   		#self.writer = csv.writer(GDFile)
		
		self.module_frame()

	def module_frame(self):
		 #criação do painel que mostra as configurações do módulo na tela principal da interface
		self.ModuleBox = Text(self.parent, bg=mygreen, height= 6, width=45, relief="flat")
		self.ModuleBox.grid(row = 1,sticky="n")

		self.ModuleBox.tag_configure('title', justify='center', font=('Kreativ', 10), foreground='white')
		self.ModuleBox.tag_configure('preferences', font=('Kreativ', 9), foreground='white')

		self.ModuleBox.insert(INSERT, "Módulo" + "\n", 'title')

		fields = 'Constante de Conversão para Volts: ' + str(self.constant), 'Deslocamento (Offset): ' + str(self.offset) + ' V', 'Ganho: ' + str(self.gain),'Taxa de Transmissão: ' + str(self.baud_rate) + ' Bps', 'Taxa de Amostragem: ' + str(self.sampling_rate)
		
		for field in fields:
			self.ModuleBox.insert(INSERT, field + "\n", 'preferences')
		self.ModuleBox.configure(state='disable')    


	# buttons can be used to start and pause plotting
	def service_buttons(self, toolbar_index):
		if toolbar_index == 0:
			self.stop = False
			if self.connect == 0:
				self.serial_data()
				#plotter.plot(self, vertical_scale, horizontal_scale)  
			elif self.connect == 1:
				self.bluetooth_data()
			else:
				tkMessageBox.showerror("Erro", "Nenhum módulo de aquisição conectado")
				return    
			plotter.plot(self, vertical_scale, horizontal_scale)        
		else:
			self.stop = True
			if toolbar_index == 2: 
				if self.connect == 0:
					self.proc.terminate()
					self.ser.close()
					self.serial_queue.close()
					print("Porta serial fechada")       

				elif self.connect == 1:
					self.procb.terminate()		
				print("Parar")    
			else:
				print("Pausar") 

	def connect_serial(self, cb_port, cb_parity, cb_RTS, cb_DTR, win):
		self.connect = 0
		
		self.port = cb_port.get()
		self.parity = cb_parity.get()       

		self.RTS = cb_RTS.get()
		self.DTR = cb_DTR.get()

		print("Conectando à porta serial %s" % self.port)
		#print self.parity
		win.destroy()

	def serial_data(self):
		self.serial_queue = Queue()
	   
		#abre a porta serial
		try:
			self.ser = serial.Serial(self.port, self.baud_rate)   #conecta à porta correta

		except:
			print("Falhou ao conectar com a porta serial")
			return    

		print("Conexão à porta serial com sucesso")
		self.ser.close()
		self.ser.open()

		if self.parity == 'Par':
			self.parity = serial.PARITY_EVEN
			print("par")
		elif self.parity == 'Ímpar':
			self.parity = serial.PARITY_ODD
		else:
			self.parity = serial.PARITY_NONE

		if self.RTS == 'Ativado':
			self.ser.setRTS(True)
			print("RTS Ativado")

		if self.DTR == 'Ativado':
			self.ser.setDTR(True)
			print("DTR Ativado")

		self.proc = Process(target=serialRead.leitura_serial_driver, args=(self.serial_queue, self.ser))
		self.proc.start()

	def connect_bluetooth(self, addr):
		self.addr = addr
		self.connect = 1	    

	def bluetooth_data(self):
		self.bluetooth_queue = Queue()

		print("Procurando por um servidor em %s" % self.addr)

		service_matches = find_service(address = self.addr)
		flag = 0

		if len(service_matches) == 0:
			print("não foi possível encontrar um serviço")
			port = 1
			flag = 1

		else:
			first_match = service_matches[0]
			port = first_match["port"]
			name = first_match["name"]
			addr = first_match["host"]
			flag = 1

			print ("conectando a \"%s\" em %s na porta %s" % (name, host, port))

		sock = BluetoothSocket(RFCOMM)
		addr = self.addr
		sock.connect((addr, port))

		print ("CONECTADO")

		self.procb = Process(target=bluetoothRead.leitura_bluetooth_driver, args=(self.bluetooth_queue, sock))
		self.procb.start()

	def save_preferences(self, win, entries):
		i = 0
		for entry in entries:
			if (entry[1].get() != ''):
				if (i == 0):
					self.constant = float(entry[1].get())
				elif (i==1):
					self.offset = float(entry[1].get())
					print(self.offset)
				elif (i==2):
					self.gain = float(entry[1].get())
				elif (i==3):
					self.baud_rate = int(entry[1].get())
				elif (i==4):
					self.sampling_rate = float(entry[1].get())	
			i+=1
		
		win.destroy()
		self.module_frame()    

	def vertical_gain(self, gain):
		self.vertical_limit = (((self.tupla[0][1] * 25.4) / dpi) * vertical_scale) / gain

		if self.horizontal_limit_1 != 0:
			self.subplot.axis([self.horizontal_limit_0, self.horizontal_limit_1, -(self.vertical_limit), self.vertical_limit])
		else:   
			self.subplot.axis([self.subplot.get_xlim()[0], self.subplot.get_xlim()[1], -(self.vertical_limit), self.vertical_limit])

		self.canvas.draw()
		print ("ganho vertical setado para %.2f mm/mV" % gain)
	 
	def horizontal_gain(self, gain):
		#limite superior
		if (self.subplot.get_xlim()[1] - self.subplot.get_xlim()[0]) == horizontal_scale:
			self.horizontal_limit_1 = ((((self.tupla[1][0] * 25.4) / dpi) * horizontal_scale) / gain) + self.subplot.get_xlim()[0]
			print (self.horizontal_limit_1)
		else:
			if self.subplot.get_xlim()[0] > 0:
				self.horizontal_limit_1 = (((self.tupla[1][0] * 25.4) / dpi) * (horizontal_scale+self.subplot.get_xlim()[0])) / gain
			else:
				self.horizontal_limit_1 = (((self.tupla[1][0] * 25.4) / dpi) * horizontal_scale) / gain

		#limite inferior
		self.horizontal_limit_0 = self.subplot.get_xlim()[0]

		if self.vertical_limit != 0:
			self.subplot.axis([self.horizontal_limit_0, self.horizontal_limit_1, -(self.vertical_limit), self.vertical_limit])
		else:
			self.subplot.axis([self.horizontal_limit_0, self.horizontal_limit_1, -(vertical_scale), vertical_scale])

		self.canvas.draw()
		print ("ganho horizontal setado para %.2f mm/s" % gain)

	def serial_ports(self):
		""" Lists serial port names

			:raises EnvironmentError:
				On unsupported or unknown platforms
			:returns:
				A list of the serial ports available on the system
		"""
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result 

	def gdfConstruct(self, win, entries, cb_valor1, cb_valor2, cb_valor3, cb_valor4, cb_valor5, cb_valor6, cb_valor7, cb_valor8):
		if self.flag_file == 1:
			self.GDFile = open("gdf_data_" + time.strftime("%H:%M") +".dat", "wb")

		i = 0
		out = ''
		versionId = 'GDF 2.10' 
		self.GDFile.write(struct.pack('8s', versionId))
		#out = ''.join(format(ord(i),'b').zfill(8) for i in versionId)

		saida = []
		saida.extend((cb_valor1.get(), cb_valor2.get(), cb_valor3.get(), cb_valor4.get(), cb_valor5.get(), cb_valor6.get(), cb_valor7.get(), cb_valor8.get()))

		j = 0	
		for entry in entries:
			if j == 0:
				self.GDFile.write(struct.pack('66s', entry[1].get()))
				#out += ''.join(format(ord(i),'b').zfill(8) for i in idP)
				
				#campo reservado
				self.GDFile.write(struct.pack('QH', 0, 0))

				i = 0
				while i<4:
					if saida[i] == 'Desconhecido':
						out += '00'
					elif saida[i] == 'Sim':
						out += '10'
					else:
						out += '01'
					i+=1

				self.GDFile.write(struct.pack('s', out))		
			
			if (j == 1 or j == 2 or j == 5):
				if entry[1].get() != '':
					self.GDFile.write(struct.pack('B', int(float(entry[1].get()))))
					#out += '{0:08b}'.format(int(float(entry[1].get())))
				if j == 2:
					out = ''
					i=0
					while i < 4:
						if i == 0:
							if saida[i] == 'Masculino':
								out += '01'
							elif saida[i] == 'Feminino':
								out+= '10'
							else:
								out += '11'	
						elif i == 1:
							if saida[i] == 'Desconhecido':
								out += '00'
							elif saida[i] == 'Destro':
								out += '01'
							elif saida[i] == 'Canhoto':
								out += '10'
							else:
								out+= '11'
						else:
							if saida[i] == 'Desconhecido':
								out += '00'
							elif unicode(saida[i]) == unicode(u'Não'):
								out += '01'
							elif saida[i] == 'Sim':
								out += '10'
							else:
								out+= '11'
						i+=1
					
					self.GDFile.write(struct.pack('s', out))

			if j == 3:
				self.GDFile.write(struct.pack('I', int(time.strftime("%d%m"))))
				self.GDFile.write(struct.pack('I', int(time.strftime("%H%M"))))

				#startdate = time.strftime("%d%m") + time.strftime("%H%M")
				#for sd in startdate:
				#	print '{0:08b}'.format(int(sd))	

				dates = entry[1].get().translate(None, "/")
				for date in dates:
					#out += '{0:08b}'.format(int(date))
					self.GDFile.write(struct.pack('>i', int(date)))	

			elif j == 4:		
				self.GDFile.write(struct.pack('6s', entry[1].get()))

			elif (j == 6 or j == 7):
				#eletrodo positions	

				#number of data records
				self.GDFile.write(struct.pack('q', -1))

				
			j+=1

		self.flag_file = 1	
		win.destroy()	   

	def save_figure(self):
		ftypes = [('PNG', '*.png')]
		filename = tkFileDialog.asksaveasfilename(initialdir = "/home", filetypes = ftypes)
		self.figure.savefig(filename, bbox_inches='tight') 

app = Application(master = root)
app.parent.configure(background = mygreen2)

principal=Menu(root)
arquivo=Menu(principal, tearoff=False)
conectar=Menu(principal, tearoff=False)
visualizacao=Menu(principal, tearoff=False)
modulo=Menu(principal, tearoff=False)

arquivo.add_command(label="Abrir", command=abrir)
root.protocol('WM_DELETE_WINDOW', sair)
arquivo.add_command(label="Salvar Como", command=salvar)
arquivo.add_command(label="Salvar Registro", command=record)
arquivo.add_command(label="Sair", command=quit)
principal.add_cascade(label="Arquivo",menu=arquivo)


conectar.add_command(label="Serial", command=conectarS)
conectar.add_command(label="Bluetooth",command=dispositivos)
principal.add_cascade(label="Conectar",menu=conectar)

#Menu Preferências
visualizacao.choicesV = Menu(visualizacao, tearoff=False)

visualizacao.choicesV.add_command(label='5 mm/mV', command = set_vertical_gain_5)
visualizacao.choicesV.add_command(label='10 mm/mV', command = set_vertical_gain_10)
visualizacao.choicesV.add_command(label='20 mm/mV', command = set_vertical_gain_20)
visualizacao.choicesV.add_command(label='40 mm/mV', command = set_vertical_gain_40)
visualizacao.choicesV.add_command(label='80 mm/mV', command = set_vertical_gain_80)

visualizacao.choicesH = Menu(visualizacao, tearoff=False)

visualizacao.choicesH.add_command(label='12,5 mm/s', command = set_horizontal_gain_12)
visualizacao.choicesH.add_command(label='25 mm/s',  command = set_horizontal_gain_25)
visualizacao.choicesH.add_command(label='50 mm/s',  command = set_horizontal_gain_50)

visualizacao.add_cascade(label='Ganho Vertical', menu=visualizacao.choicesV)
visualizacao.add_cascade(label='Ganho Horizontal', menu=visualizacao.choicesH)
principal.add_cascade(label="Visualização",menu=visualizacao)

#Menu Módulo
modulo.add_command(label="Preferências", command=module_preferences)
principal.add_cascade(label="Módulo", menu=modulo)

principal.add_command(label="Ajuda",command=ajuda)
root.configure(menu=principal)

directory = os.path.dirname(os.path.abspath(__file__))

img = PhotoImage(file= directory + '/icons/Interface.png')
root.tk.call('wm', 'iconphoto', root._w, img)

app.master.title("Sistema para visualização de sinais bioelétricos")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
app.master.geometry('%dx%d+0+0' % (width,height))
mainloop()