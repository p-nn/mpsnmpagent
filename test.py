from serverudpsnmp2 import ServerUdpSnmp2, const2
from time import sleep
import sys

#from serverudpsnmpsmart import ServerUdpSnmpSmart
from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR, ASN1_OCTSTR, ASN1_OID


#snmpwalk -d -v1 -c public localhost:7777 0

class ServerUdpSnmpCustom(ServerUdpSnmp2):
    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0"), ASN1_OCTSTR
    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0"), ASN1_OID #"1.3.6.1.4.1.318.1.3.1"
    SNMP_OID_temperatureC   = const2("1.3.6.1.3.2016.5.1.0"), ASN1_INT

    #ServerUdpSnmp2.NVS[SNMP_OID_temperatureC[0]]=      '22'

    def handle_get(self, oid, community):
        res = None
        if oid == self.SNMP_OID_sysDescr[0]: #calculate response
            res = "SuperDevice"
            print("get:oid {} is sysDescr".format(oid))
        if oid == self.SNMP_OID_sysObjectID[0]: #calculate response
            res = "1.3.6.1.4.1.318.1.3.1"
            print("get:oid {} is sysObjectID".format(oid))
        if oid == self.SNMP_OID_temperatureC[0]: #calculate response
            res = 25
            print("get:oid {} is temperatureC".format(oid))

        return res


s = ServerUdpSnmpCustom('', 7777)
#s = ServerUdpSnmpSmart('', 7777,'/dev/ttyS0')
s.start()

sleep(10)
s.running = False
sleep(2)
sys.exit()
#tt = b'100.0'
#ttt = tt.decode().split('.')[0]

#print(int(ttt)+1)
