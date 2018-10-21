"""
@author: Pedro Augusto
UFMS - Universidade Federal de Mato Grosso do Sul
"""
from multiprocessing import Process, Queue, Pipe
import struct

def leitura(q):
	while True:
		valor = struct.unpack('H',q.recv())[0]
		#print bin(valor) 
		highByte = (valor & 16128) >> 2
		lowByte = valor & 255
		res = (highByte | lowByte)
		print ("Valor lido da Serial:",res)