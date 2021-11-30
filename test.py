from serverudpsnmp import ServerUdpSnmp, const2
from time import sleep
import sys

from serverudpsnmpsmart import ServerUdpSnmpSmart
from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR
#snmpwalk -d -v1 -c public localhost:7777 0

class ServerUdpSnmpCustom(ServerUdpSnmp):
    SNMP_OID_temperatureC   = const2("1.3.6.1.3.2016.5.1.0")

    def handle_get(self, oid, community):
        if oid == self.SNMP_OID_temperatureC: #calculate response

            res = ASN1_INT, 25, SNMP_ERR_NOERROR
            print("get:oid {} is temperatureC".format(oid))
        else: #from constants _SNMP_OIDs
            res = super().handle_get(oid)
        return res


#s = ServerUdpSnmpCustom('', 7777)
s = ServerUdpSnmpSmart('', 7777,'/dev/ttyS0')
s.start()

sleep(15)
s.running = False
sleep(2)
sys.exit()
#tt = b'100.0'
#ttt = tt.decode().split('.')[0]

#print(int(ttt)+1)