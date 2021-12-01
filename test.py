import collections

from serverudpsnmp2 import ServerUdpSnmp2, const2
from time import sleep
import sys

#from serverudpsnmpsmart import ServerUdpSnmpSmart
from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR, ASN1_OCTSTR, ASN1_OID


#snmpwalk -v1 -Ofn -Ir -Ci -c public localhost:7777


class ServerUdpSnmpCustom(ServerUdpSnmp2):
    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1"),    ASN1_OCTSTR
    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2"),    ASN1_OID #"1.3.6.1.4.1.318.1.3.1"
    SNMP_OID_sysName        = const2("1.3.6.1.2.1.1.5"),    ASN1_OCTSTR
    SNMP_OID_temperatureC   = const2("1.3.6.1.3.2016.5.1"), ASN1_INT

    #NVS = object()
    #ServerUdpSnmp2.NVS[SNMP_OID_temperatureC[0]]=      '22'
    #reverse_order = True
    def handle_get(self, oid, community):
        print("handle_get: community=",community)
        res = None
        if oid == self.SNMP_OID_sysDescr[0]: #calculate response
            res = "SuperDevice"
            print("get:oid {} is sysDescr".format(oid))
        if oid == self.SNMP_OID_sysObjectID[0]: #calculate response
            res = "1.3.6.1.4.1.318.1.3.1"
            print("get:oid {} is sysObjectID".format(oid))
        if oid == self.SNMP_OID_sysName[0]: #calculate response
            res = "SuperDeviceName"
            print("get:oid {} is sysName".format(oid))
        if oid == self.SNMP_OID_temperatureC[0]: #calculate response
            res = 25
            print("get:oid {} is temperatureC".format(oid))

        return res

    def handle_set(self, oid, community, value):
        print(oid, community, value)
        value_verifed = value
        return value_verifed

s = ServerUdpSnmpCustom('', 7777)
#try:
#    from machine import PWRON_RESET
#    s.reverse_order = False

#except:
#   # s.reverse_order = True #
#    print("reverse order attributes")

#s = ServerUdpSnmpSmart('', 7777,'/dev/ttyS0')#
s.start()

sleep(10)
s.running = False
print("We stop ... ")
sleep(1)
sys.exit()



