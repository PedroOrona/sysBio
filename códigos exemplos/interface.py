# coding=UTF-8
from Tkinter import *
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import random, sin, exp

def abrir(): print "abrir"
def salvar(): print "salvar"
def ajuda() : print "ajuda"

class Application(Frame):
  def __init__(self, master=None):
    Frame.__init__(self)
    self.top = Frame()
    self.top.grid()
    self.top.update_idletasks()

    self.x = 0
    self.i = 0
    self.delta_i = 1
    self.update = 4
    # to speed things up, never plot more than n_points on screen
    self.n_points = 500
    self.n_data = 10000     # maximum number of points to acquire
    self.xy_data = []

    self.figure = pyplot.figure()
    # figsize (w,h tuple in inches) dpi (dots per inch)
    self.figure.set_size_inches((9,6), forward=True)
    self.subplot = self.figure.add_subplot(211)

    self.line, = self.subplot.plot([],[]) # initialize line to be drawn
    # Note: The comma after line is because the right hand size returns
    #   a one element list, and we want to unpack that single element
    #   into line, not assign the list to line.
    self.text = pyplot.figtext(0.05,0.25,"") # initialize text section

    self.canvas = FigureCanvasTkAgg(self.figure, master=self.top)
    self.canvas.get_tk_widget().grid(row=3,column=0,columnspan=3)

    self.button_text = ['Start','Pause']
    self.buttons = [None] * len(self.button_text)

    for button_index in range(len(self.button_text)) :
	button_id = Button(self.top,text=self.button_text[button_index])
	button_id.grid(row=0, column=button_index)
	self.buttons[button_index] = button_id

	def button_handler(event, self=self, button=button_index):
	    return self.service_buttons(button)

	button_id.bind("<Button-1>", button_handler)

  # buttons can be used to start and pause plotting
  def service_buttons(self, toolbar_index):
    if toolbar_index == 0 :
	self.stop = False
	self.plotter()
    else:
	self.stop = True

  # while in start, check if stop is clicked, if not, call blink recursivly
  def plotter(self):
    if not self.stop :
	self.x += 0.1
	self.y = exp(-self.i*0.005)*sin(self.x)+0.1*random.randn()
	self.xy_data += [[self.x,self.y]]
	# If there are many data points, it is a waste of time to plot all
	#   of them once the screen resolution is reached,
	#   so when the maximum number of points is reached,
	#   halve the number of points plotted. This is repeated
	#   every time the number of data points has doubled.
	if self.i == self.n_points :
	    self.n_points *= 2
	    # frequency of plotted points
	    self.delta_i *= self.n_points/self.i
	    self.update = max(self.delta_i, self.update)
	    print("updating n_rescale = ",\
		self.n_points, self.update, self.delta_i)
	# drawing the canvas takes most of the CPU time, so only update plot
	#   every so often
	if self.i == self.n_data-1 or not (self.i % self.update)  :
	    # remove previous version of line plot
	    self.subplot.lines.remove(self.line)
	    self.figure.texts.remove(self.text)
	    self.line, = self.subplot.plot(
			[row[0] for row in self.xy_data[0::self.delta_i]],
			    [row[1] for row in self.xy_data[0::self.delta_i]],
			    color="blue")
	    self.text = pyplot.figtext(0.05,0.25,
			      "Point # " + str(self.i+1) +
			      "\nx,y = " + str(self.x) + ", " + str(self.y))
	self.i += 1
	# stop if desired number of points plotted
	if self.i == self.n_data :
	    self.service_buttons(1)
	self.canvas.draw()
	self.canvas.get_tk_widget().update_idletasks()
	self.after(2,self.plotter)	

root=Tk()
root.wm_title("Gráfico em tempo real") # title for window

principal=Menu(root)
arquivo=Menu(principal, tearoff=False)
arquivo.add_command(label="Abrir", command=abrir)
arquivo.add_command(label="Salvar Como", command=salvar)
arquivo.add_command(label="Sair", command=quit)
principal.add_cascade(label="Arquivo",menu=arquivo)
principal.add_command(label="Ajuda",command=ajuda)
root.configure(menu=principal)

#img = PhotoImage(file='/media/pedro/7BE95CA9735ED5D4/Pedro/UFMS/TCC/heart1.png')
#root.tk.call('wm', 'iconphoto', root._w, img)

app = Application()
app.master.title("Interface Gráfica")
app.master.geometry("800x600+100+100")
mainloop()