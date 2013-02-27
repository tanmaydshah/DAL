import matplotlib
import pylab
matplotlib.use('GTK') # do this before importing pylab
import matplotlib.pyplot as plt
import random
import serial, re
import time
import math
import numpy



ser=serial.Serial()
ser.baudrate=57600
ser.port='/dev/rfcomm0'
ser.timeout=2
ser.open()


#ser1=serial.Serial()
#ser1.baudrate=57600
#ser1.port='/dev/rfcomm1'
#ser1.timeout=2
#ser1.open()

fig = plt.figure()
ax = fig.add_subplot(111)
ay = fig.add_subplot(111)
az = fig.add_subplot(111)
ar = fig.add_subplot(111)
#ay = fig.add_subplot(110)

x = range(50)
xx = [random.random() for i in x]
yy = [random.random() for i in x]
zz = [random.random() for i in x]
rr = [random.random() for i in x]

line1, = ax.plot(x,xx)
line2, = ay.plot(x,yy)
line3, = az.plot(x,zz)
line4, = ar.plot(x,rr)


#Filtering



def animate(*args):
		nx = len(xx)
		ny = len(yy)
		nz = len(zz)
		nr = len(rr)
		d = 0
		x0=0
		y0=0
		z0=0
		r0=0
		r1=0

		dt=(1.0/20)
		RC=0.3
		alpha=dt/(RC+dt)
		count=0
		while 1:
			ser.write('XRA')
			#ser1.write('XRA')
			time.sleep(0.001)
			
			t=ser.readline()
			#u=ser1.readline()
			acc = re.findall("[+/-]\d+",t)
			#acc1=re.findall("[+/-]\d+",u)
			#if acc[2]<0:
			#	print acc
			#mx=float(int(acc[0]))
			#my=float(int(acc[1]))
			#mz=float(int(acc[2]))
			#print mx
			#print my
			#print mz
#			sx=float((alpha*(float(int(acc[0]))))+((1.0-alpha)*x0))
#			sy=float((alpha*(float(int(acc[1]))))+((1.0-alpha)*y0))
#			sz=float((alpha*(float(int(acc[2]))))+((1.0-alpha)*z0))
			#sx=smooth(int(acc[0]))
			#sy=smooth(int(acc[1]))
			#sz=smooth(acc[2])
			
			#if sr>80:
			#	print sr
			if len(acc) == 3:
				sx=float((alpha*(float(int(acc[0]))))+((1.0-alpha)*x0))
				sy=float((alpha*(float(int(acc[1]))))+((1.0-alpha)*y0))
				sz=float((alpha*(float(int(acc[2]))))+((1.0-alpha)*z0))
				sr=float(math.sqrt(math.pow(sx,2.0)+math.pow(sy,2.0)+math.pow(sz,2.0)))
				tx=(sx/200)+.5
				ty=(sy/200)+.5
				tz=(sz/200)+.5
				#tz=(float(int(acc[2]))/200)+.5
				
				tr=(float((sr))/200)+.5
				if tx>1:
					tx=1
				if ty>1:
					ty=1
				if tz>1:
					tz=1
				if tr>1:
					tr=1
				if sz<54.00:				
					if r1<sr and r1<r0:
						print 'CLICK'
						print 'resultant : '+str(int(sr))
						print 'X : ' + str(int(sx))
						print 'Y : ' + str(int(sy))
						print 'Z : ' + str(int(sz))
						time.sleep(0.1)
						count=count+1
						print 'counter : ' + str(count)
				xx.append(tx)
				yy.append(ty)
				zz.append(tz)
				rr.append(tr)
				x0=sx
				y0=sy
				z0=sz
				r0=r1
				r1=sr
				
			else:
				xx.append(0)
				yy.append(0)
				zz.append(0)
				rr.append(0)
			nx += 1
			ny += 1
			nz += 1
			nr += 1
			d += 10
			
			
			
			line1.set_data(range(nx-30, nx), xx[-30:])
			line2.set_data(range(ny-30, ny), yy[-30:])
			line3.set_data(range(nz-30, nz), zz[-30:])
			line4.set_data(range(nr-30, nr), rr[-30:])
			ax.set_xlim(nx-31, nx-1)
			ay.set_xlim(ny-31, ny-1)
			az.set_xlim(nz-31, nz-1)
			ar.set_xlim(nr-31, nr-1)
			fig.canvas.draw()

fig.canvas.manager.window.after(1000, animate)
plt.show()
while(1):
		ff=1
