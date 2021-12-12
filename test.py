import collections

import apcsmartups
import serverudpsnmp
import mibs

from time import sleep
import sys

from serverudpsnmpsmart import ServerUdpSnmpSmart
from serverudpsnmp import ServerUdpSnmp
#snmpwalk -v1 -Ofn -Ir -Ci -c public localhost:7777


class ServerUdpSnmpCustom(ServerUdpSnmp):
    #ordered oids

    def __init__(self, local_ip='', local_port=161):
        super().__init__(local_ip, local_port)
        self.add_oid(mibs.SNMP_OID_sysDescr)
        self.add_oid(mibs.SNMP_OID_sysObjectID)
        self.add_oid(mibs.SNMP_OID_sysName)

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

s = ServerUdpSnmpSmart('', 7777, tx=32, rx=33)#
s.start()
#sleep(90)
#while(True):
#    pass
#s.running = False
#print("We stop ... ")
#sleep(1)
#sys.exit()




    #https://sourceforge.net/p/apcupsd/mailman/apcupsd-commits/?viewmonth=200505
#/usr/local/etc/nut/driver.list
#"Various"       "ups"   "3"     "(various)"     "SNMP - RFC 1628"       "snmp-ups (experimental)"

