import sys
import serial
import re
import time
ser=serial.Serial()
ser.baudrate=57600
ser.port='/dev/rfcomm0'
ser.timeout=2
ser.open()

while 1:
	ser.write('XRA')
	time.sleep(0.001)
	t=ser.readline()
	acc = re.findall("[+/-]\d+",t)
	sys.stdout.write(acc)
	sys.stdout.flush()
	
