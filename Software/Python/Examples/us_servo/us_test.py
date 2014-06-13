from gopigo import *
import sys
from collections import Counter
import math

def us_map():
	debug =0
	num_of_readings=45
	incr=180/num_of_readings
	ang_l=[0]*(num_of_readings+1)
	dist_l=[0]*(num_of_readings+1)
	x=[0]*(num_of_readings+1)
	y=[0]*(num_of_readings+1)

	buf=[0]*40
	ang=0
	lim=250
	index=0
	sample=2
	print "Getting the data"
	while True:
		#for i in range (21):
		for i in range(sample):
			dist=us_dist(15)
			#print dist
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim

		max=Counter(buf).most_common()
		rm=-1
		for i in range (len(max)):
			if max[i][0] <> lim and max[i][0] <> 0:
				rm=max[i][0]
				break
		if rm==-1:
			rm=lim
		
		if debug==1:
			print index,ang,rm
		#print '.',
		ang_l[index]=ang
		dist_l[index]=rm
		index+=1

		servo(ang)
		ang+=incr
		if ang>180:
			break
			
	grid_size=51
	for i in range(num_of_readings+1):
		x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/10)#+grid_size/2
		y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/10
	for i in range(num_of_readings+1):
		x[i]=(grid_size/2)-x[i]
		y[i]=(grid_size/2)-y[i]

	grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)] 
	for i in range (num_of_readings+1):
		if dist_l[i]<>lim:
			grid[y[i]][x[i]]=1
	fence='-'*(grid_size+1)
	print "Map:"
	print fence*2
	for i in range(grid_size/2):
		print "|",
		for j in range (grid_size):
			if (j==grid_size/2)and i==(grid_size/2)-1:
				print 'x',
			elif grid[i][j]==0:
				print ' ',
			else:
				print 'o',
		print "|"
	print fence*2
	return min(dist_l)
	
while True:
	enc_tgt(1,1,36)
	fwd()
	#for i in range(10):
	while True:
		if read_status() == 0:
			break
		time.sleep(1)
	if us_map() <20:
		break