
import serverudpsnmp
from time import sleep
import sys

from serverudpsnmpsmart import ServerUdpSnmpSmart
from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR

s = serverudpsnmp.ServerUdpSnmp('', 7777)
#s = ServerUdpSnmpSmart('', 7777,'/dev/ttyS0')
s.start()
sleep(15)
s.running = False
sleep(2)
sys.exit()
#tt = b'100.0'
#ttt = tt.decode().split('.')[0]

#print(int(ttt)+1)


print("Hello!!!")