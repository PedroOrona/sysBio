#import the different modules like time,multiprocessing
# coding=UTF-8
"""
@author: Pedro Augusto
UFMS - Universidade Federal de Mato Grosso do Sul
"""
import tkinter
from tkinter import messagebox as tkMessageBox
import serial
import struct
import principal
import time
from multiprocessing import Process, Queue, Pipe
from time import sleep

def leitura_serial_driver(q, ser):
     #abre a porta serial e lê seu valor
     while True:
        valor = ser.read(2)
        sinc = struct.unpack('H',valor)[0]
        if sinc < 32768:
            valor = ser.read(1)
            valor = ser.read(2)
        #print ' '.join(format(ord(x), 'b') for x in valor)    
        q.put(valor)    


def cod_serial(valor, constant, offset, gain):
    highByte = (valor & 16128) >> 2
    lowByte = valor & 255
    res = (((highByte | lowByte) * constant) + offset)/gain

    return res

"""def main():
    parent_conn, child_conn = Pipe(duplex=False)
    
    procs = []
    procs.append(Process(target=leitura_serial_driver, args=(child_conn,)))
    procs.append(Process(target=principal.leitura, args=(parent_conn,)))
    map(lambda x: x.start(), procs)
    map(lambda x: x.join(), procs)


    Label(win, text="Portas disponíveis").pack()

    frame = Frame(win)
    frame.pack()

    listNodes = Listbox(frame, width=25, height=5, font=("Helvetica", 12))
    listNodes.pack(side="left", fill="y")

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listNodes.yview)
    scrollbar.pack(side="right", fill="y")

    result = app.serial_ports()
    for port in result:
        listNodes.insert(END, "%s" % port)

if __name__ == "__main__":
    main()"""
