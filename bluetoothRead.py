# coding=UTF-8
"""
@author: Pedro Augusto
UFMS - Universidade Federal de Mato Grosso do Sul
"""
from bluetooth import *
import bluetooth
from multiprocessing import Process, Queue, Pipe
import struct
import sys

def cod_bluetooth(valor, constant, offset, gain):
    highByte = (valor & 16128) >> 2
    lowByte = valor & 255
    res = (((highByte | lowByte) * constant) + offset)/gain

    return res

def leitura_bluetooth_driver(p, sock):
    #Protocolo de leitura
    while True:
        valor = sock.recv(2)
        sinc = struct.unpack('H',valor)[0]
        if sinc < 32768:
            valor = sock.recv(1)
            valor = sock.recv(2)
        #print ' '.join(format(ord(x), 'b') for x in valor)    
        p.put(valor)   
    
    sock.close()
    print("DESCONECTADO")
