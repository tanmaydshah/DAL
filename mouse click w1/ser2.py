import sys
import serial
import re
import time
ser1=serial.Serial()
ser1.baudrate=57600
ser1.port='/dev/rfcomm1'
ser1.timeout=2
ser1.open()

while 1:
	ser1.write('XRA')
	time.sleep(0.001)
	u=ser1.readline()
	acc1 = re.findall("[+/-]\d+",u)
	sys.stdout.write(acc1)
	sys.stdout.flush()
