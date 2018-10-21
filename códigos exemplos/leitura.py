#import the different modules like time,multiprocessing
# coding=UTF-8
import serial
from multiprocessing import Process, Pipe
porta = '/dev/ttyACM0'
baud_rate = 9600

#Define the two parallel processes:
def main():
    #abre a porta serial e lê seu valor
    print "Trying to connect to Arduino"
    while True:
    	try:
	  ser = serial.Serial(porta, 9600)   #connect to the right port
	  valor = ser.readline()
	  print "Valor lido da Serial: ", valor
	    
	except:
	  print "Failed to connect to Arduino"
	  return

if __name__ == "__main__":
	main()