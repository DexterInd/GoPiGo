from gopigo import *

enc_tgt(1,0,72)
fwd()
i=0
while True:
#time.sleep(1)
	#print i,volt()
	print read_status()
	i+=1
	time.sleep(.1)