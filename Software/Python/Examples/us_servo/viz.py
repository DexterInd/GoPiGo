from gopigo import *
import sys
from collections import Counter
import math
num_of_readings=45
incr=180/num_of_readings
ang_l=[0]*(num_of_readings+1)
dist_l=[0]*(num_of_readings+1)
x=[0]*(num_of_readings+1)
y=[0]*(num_of_readings+1)

buf=[0]*10
ang=0
lim=250
index=0
sample=5
while True:
	#for i in range (21):
	for i in range(sample):
		dist=us_dist(15)
		if dist<lim and dist>=0:
			buf[i]=dist
		else:
			buf[i]=lim
		#time.sleep(.01)
	#for i in range(10):
	#	print buf[i],
	#print ""
	
	max=Counter(buf).most_common()
	rm=0
	for i in range (len(max)):
		if max[i][0] <> lim:
			rm=max[i][0]
			break
	if rm==0:
		rm=lim
	print index,ang,rm
	ang_l[index]=ang
	dist_l[index]=rm
	index+=1
	#print rm
	servo(ang)
	ang+=incr
	if ang>180:
		break
	#time.sleep(.2)
print ang_l,dist_l
grid_size=51
for i in range(num_of_readings+1):
	x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/10)#+grid_size/2
	y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/10
print "x"
print x
print "y"
print y
for i in range(num_of_readings+1):
	x[i]=(grid_size/2)-x[i]
	y[i]=(grid_size/2)-y[i]
print "x"
print x
print "y"
print y


grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)] 
for i in range (num_of_readings+1):
	grid[y[i]][x[i]]=1

for i in range(grid_size/2):
	for j in range (grid_size):
		if j==grid_size/2 and i==(grid_size/2)-1:
			print 'x'
		elif grid[i][j]==0:
			print ' ',
		else:
			print 'o',
	print ""
			