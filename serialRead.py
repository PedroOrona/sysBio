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
