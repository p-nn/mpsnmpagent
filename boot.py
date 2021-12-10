# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from machine import Pin
p4 = Pin(4, Pin.IN, Pin.PULL_UP)
p4v = p4.value()
if p4.value()==1:
	print('GPIO4=',p4v,'=>do boot2.py')
	execfile('boot2.py')
else:
	print('GPIO4=',p4v,'=>skip boot2.py')
	

