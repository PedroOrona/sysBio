# coding=UTF-8
"""
@author: Pedro Augusto
UFMS - Universidade Federal de Mato Grosso do Sul
"""
import struct
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import serialRead
import bluetoothRead

def plot(self, vertical_scale, horizontal_scale):
    tam = 90
    flag = 1

    
    #writer.writerow(('Time(s)', 'Signal(mV)'))
    time = 1/(float(self.sampling_rate))
    #print time
    
    while not self.stop :
        i = 0
        #trata o valor recebido caso o usuário tenha realizado uma conexão Serial        
        if (self.connect == 0):
            if flag == 2 or tam < self.serial_queue.qsize():
                tam = int(20 * self.serial_queue.qsize())
                #tam = int(tam + (tam/1.5))
                if tam > 6000:
                    tam = int(tam/3)
                print (tam)
            while i<tam:
                valor = struct.unpack('H',self.serial_queue.get())[0]
                self.y = serialRead.cod_serial(valor, self.constant, self.offset, self.gain)
                #self.y = (valor * self.constant) + self.offset
                
                self.GDFile.write(struct.pack('II', self.x, self.y))

                #print self.y

                self.xy_data += [[self.x,self.y]]
                self.x += time
                i += 1
                if self.serial_queue.empty():
                    i = tam

        #trata o valor recebido caso o usuário tenha realizado uma conexão Bluetooth    
        elif (self.connect == 1):
            if flag == 2 or tam < self.bluetooth_queue.qsize():
                tam = int(20 * self.bluetooth_queue.qsize())
                #tam = int(tam + (tam/1.5))
                print (tam)
            while i<tam:
                valor = struct.unpack('H',self.bluetooth_queue.get())[0]  
                self.y = bluetoothRead.cod_bluetooth(valor, self.constant, self.offset, self.gain)
                #writer.writerow( (self.x, self.y) )
                print (self.y)
                self.xy_data += [[self.x,self.y]]
                self.x += time
                i += 1
                if self.bluetooth_queue.empty():
                    i = tam

        if self.x > self.subplot.get_xlim()[1]:
            if self.horizontal_limit_1 != 0:
                CurrentXAxis=np.arange(self.x-self.horizontal_limit_1,self.x,1)
            else:
                CurrentXAxis=np.arange(self.x-horizontal_scale,self.x,1)

            if self.vertical_limit != 0:
                self.subplot.axis([CurrentXAxis.min(),CurrentXAxis.max()+1,-(self.vertical_limit), self.vertical_limit])
            else:
                #self.subplot.axis([CurrentXAxis.min(),CurrentXAxis.max()+1,-(vertical_scale), vertical_scale])
                self.subplot.axis([CurrentXAxis.min(),CurrentXAxis.max()+1,0, vertical_scale])

        self.subplot.lines.remove(self.line)

        x_list = [x for [x, y] in self.xy_data]
        y_list = [y for [x, y] in self.xy_data]

        #self.line, = self.subplot.plot(x_list, y_list, color="#00CD00", markevery=76)
        self.line, = self.subplot.plot(x_list, y_list, color="#00CD00")
        self.subplot.draw_artist(self.subplot.patch)
        self.subplot.draw_artist(self.line)
        self.canvas.draw_idle()
        self.canvas.flush_events()

        if flag == 1:
            flag += 1
        elif flag == 2:
            flag = 0   

        #limpa uma parte lista de dados x,y
        if len(self.xy_data) > 1000 and self.horizontal_limit_1 == 0:
            del self.xy_data[:len(self.xy_data) - int(horizontal_scale/time)*2]

    #limpa toda a lista
    print ("lista limpa")
    del self.xy_data[:]

    self.GDFile.close()
        