import time
from serverudp import ServerUdp
from usnmp import SNMP_GETREQUEST, SNMP_GETNEXTREQUEST, SNMP_SETREQUEST, SNMP_GETRESPONSE, SnmpPacket, ASN1_OCTSTR, SNMP_ERR_NOSUCHNAME
from usnmp_codec import ASN1_NULL, ASN1_OID, SNMP_ERR_NOERROR
# https://github.com/PinkInk/upylib/tree/master/usnmp
try:
    const2('')
except:
    def const2(v):
        return v

try:
    from ucollections import OrderedDict
except:
    try:
        from collections import OrderedDict
    except:
        pass

class ServerUdpSnmp(ServerUdp):
    #debug = True
    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0") # linux mbrowse
    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0")
    SNMP_OID_sysContact     = const2("1.3.6.1.2.1.1.4.0")
    SNMP_OID_sysName        = const2("1.3.6.1.2.1.1.5.0")
    SNMP_OID_sysLocation    = const2("1.3.6.1.2.1.1.6.0")
    SNMP_OID_sysServices    = const2("1.3.6.1.2.1.1.7.0")

    _SNMP_OIDs = OrderedDict()#ASN.1 sequence and SNMP derivatives #IMPORTANT manual order need for getnext

    _SNMP_OIDs[SNMP_OID_sysDescr]       = ASN1_OCTSTR, "sysDescr"
    _SNMP_OIDs[SNMP_OID_sysObjectID]    = ASN1_OID, "sysObjectID"
    _SNMP_OIDs[SNMP_OID_sysContact]     = ASN1_OCTSTR, "sysContact"
    _SNMP_OIDs[SNMP_OID_sysName]        = ASN1_OCTSTR, "sysName"
    _SNMP_OIDs[SNMP_OID_sysLocation]    = ASN1_OCTSTR, "sysLocation"
    _SNMP_OIDs[SNMP_OID_sysServices]    = ASN1_OCTSTR, "sysServices"

    def handle_udp(self, bytes):
        message = bytes[0]
        address = bytes[1]
        greq = SnmpPacket(message)
        gresp = SnmpPacket(type=SNMP_GETRESPONSE, community=greq.community, id=greq.id)
        for oid in greq.varbinds:
            print(oid, " ", greq.varbinds[oid])
            if greq.type==SNMP_GETREQUEST:
                self._handle_get(oid,gresp)
            if greq.type==SNMP_GETNEXTREQUEST:
                self.handle_get_next(oid,gresp)
            if greq.type==SNMP_SETREQUEST:
                self.handle_set(oid,gresp)
        #        gresp.varbinds[oid] = usnmp.SNMP_COUNTER, 3523441234

        clientMsg = "Message from Client:{}".format(greq.type)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        # Sending a reply to client
        bytesToSend = gresp.tobytes()
        print("sending:{}".format(gresp))
        self.socket.sendto(bytesToSend, address)
        print(time.time())
        return True

    def handle_get(self, oid, community):
        if oid in self._SNMP_OIDs.keys(): #from constants
            res = self._SNMP_OIDs[oid][0],self._SNMP_OIDs[oid][1], SNMP_ERR_NOERROR
        else:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)
        return res

    def _handle_get(self, oid, gresp):#usnmp.SNMP_GETREQUEST
        res = self.handle_get(oid, gresp.community)
        gresp.varbinds[oid] = res[0], res[1]
        gresp.err_status = res[2]

    def handle_set(self, oid, community, vtype, value):
        if oid in self._SNMP_OIDs.keys(): #from constants
            res = self._SNMP_OIDs[oid][0],self._SNMP_OIDs[oid][1], SNMP_ERR_NOERROR
        else:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)
        return res


    def _handle_set(self, oid, gresp):
        print("set:{}".format(oid))
        self.handle_set(oid,gresp.community,gresp.varbinds[oid][0],gresp.varbinds[oid][1])


    def handle_get_next(self, oid, gresp):
        f = oid=="0"
        #o = None
        result = None
        #    if oid in _SNMP_OIDs.keys():
        #        print("get_next: oid {} exists in list".format(oid))
        for toid in self._SNMP_OIDs:
            if f:
                result = toid
                print("get_next: next oid for {} exists in list - {}".format(oid,toid))
                break
            if toid.startswith(oid) & (toid != oid):
                result = toid
                print("get_next: next oid for {} exists in list - {}".format(oid,toid))
                break
            if toid == oid:
                f = True

        print("next:{}->{}".format(oid,result))
        if result != None:
            self._handle_get(result,gresp)
        else:
            gresp.err_status = SNMP_ERR_NOSUCHNAME
            gresp.err_id = 1
            # result = o
        return result



