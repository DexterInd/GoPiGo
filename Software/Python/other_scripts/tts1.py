#import sys
from subprocess import call
 
def sound(spk):
	cmd_beg="espeak --stdout '"
	cmd_end="' | aplay"
	print cmd_beg+spk+cmd_end
	call ([cmd_beg+spk+cmd_end], shell=True)

sound("Hi There")

