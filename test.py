import collections

import mibs
from serverudpsnmp2 import ServerUdpSnmp2, const2
from time import sleep
import sys

try:
    from ucollections import OrderedDict
except:
    try:
        from collections import OrderedDict
    except:
        pass
from serverudpsnmpsmart import ServerUdpSnmpSmart
from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR, ASN1_OCTSTR, ASN1_OID


#snmpwalk -v1 -Ofn -Ir -Ci -c public localhost:7777


class ServerUdpSnmpCustom(ServerUdpSnmp2):
    #ordered oids
    OIDS = OrderedDict()
    OIDS[mibs.SNMP_OID_sysDescr[0]]=mibs.SNMP_OID_sysDescr[1]
    OIDS[mibs.SNMP_OID_sysObjectID[0]]=mibs.SNMP_OID_sysObjectID[1]
    OIDS[mibs.SNMP_OID_sysName[0]]=mibs.SNMP_OID_sysName[1]
   # OIDS[mibs.SNMP_OID_temperatureC[0]]=mibs.SNMP_OID_temperatureC[1]

    #NVS = object()
    #ServerUdpSnmp2.NVS[SNMP_OID_temperatureC[0]]=      '22'
    #reverse_order = True
    def handle_get(self, oid, community):
        print("handle_get: community=",community)
        res = None
        if oid == mibs.SNMP_OID_sysDescr[0]: #calculate response
            res = "SuperDevice"
            print("get:oid {} is sysDescr".format(oid))
        if oid == mibs.SNMP_OID_sysObjectID[0]: #calculate response
            res = "1.3.6.1.4.1.318.1.3.1"
            print("get:oid {} is sysObjectID".format(oid))
        if oid == mibs.SNMP_OID_sysName[0]: #calculate response
            res = "SuperDeviceName"
            print("get:oid {} is sysName".format(oid))
        if oid == mibs.SNMP_OID_temperatureC[0]: #calculate response
            res = 25
            print("get:oid {} is temperatureC".format(oid))

        return res

    def handle_set(self, oid, community, value):
        print(oid, community, value)
        value_verifed = value
        return value_verifed

#s = ServerUdpSnmpCustom('', 7777)
#try:
#    from machine import PWRON_RESET
#    s.reverse_order = False

#except:
#   # s.reverse_order = True #
#    print("reverse order attributes")

s = ServerUdpSnmpSmart('', 7777,'/dev/ttyS0')#
s.start()
sleep(30)
s.running = False
print("We stop ... ")
sleep(1)
sys.exit()




