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

class ServerUdpSnmp2(ServerUdp):
    #debug = True
    #const starts with 'SNMP_OID_' is tuple, "sysDescr" # linux mbrowse, "sysObjectID"
    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0"),ASN1_OCTSTR
    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0"),ASN1_OID
    NVS = OrderedDict() #storage values may be external later
    NVS[SNMP_OID_sysDescr[0]]=      'SysDescr2'
    NVS[SNMP_OID_sysObjectID[0]]=   'sysObjectID'
#    _SNMP_OIDs = OrderedDict()#ASN.1 sequence and SNMP derivatives #IMPORTANT manual order need for getnext

#    _SNMP_OIDs[SNMP_OID_sysDescr]       = ASN1_OCTSTR, "sysDescr"
#    _SNMP_OIDs[SNMP_OID_sysObjectID]    = ASN1_OID, "sysObjectID"

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
        res = None
        for attr_name in self.__class__.__dict__:
            if attr_name.startswith('SNMP_OID_'):
                attr_value = self.__getattribute__(attr_name)
                if attr_value[0] == oid: #from constants
                    print("handle_get: ",attr_name, "=", attr_value)
                    res = attr_value[1], self.NVS[attr_value[0]], SNMP_ERR_NOERROR
                    break
        if res == None:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)
        return res

    def _handle_get(self, oid, gresp):#usnmp.SNMP_GETREQUEST
        res = self.handle_get(oid, gresp.community)
        gresp.varbinds[oid] = res[0], res[1]
        gresp.err_status = res[2]

    def handle_set(self, oid, community, vtype, value):
        res = None
        for attr_name in self.__class__.__dict__:
            if attr_name.startswith('SNMP_OID_'):
                attr_value = self.__getattribute__(attr_name)
                print(attr_name, "=", attr_value)
                if attr_value[0] == oid: #from constants
                    found = True
                    if attr_value[0] == vtype:
                        NVS[attr_value[0]]=value
                        res = (vtype, value, SNMP_ERR_NOERROR)
                    else:
                        print("wrong type:",attr_value[0],"<>",vtype)
                        res = (vtype, value, SNMP_ERR_BADVALUE)

        if res is None:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)
        return res


    def _handle_set(self, oid, gresp):
        print("set:{}".format(oid))
        res = self.handle_set(oid,gresp.community,gresp.varbinds[oid][0],gresp.varbinds[oid][1])
        gresp.varbinds[oid] = res[0], res[1]
        gresp.err_status = res[2]


    def handle_get_next(self,oid, gresp):
        f = oid=="0"
        #o = None
        result = None
        print("get_next: next oid for {}:".format(oid))
        #    if oid in _SNMP_OIDs.keys():
        #        print("get_next: oid {} exists in list".format(oid))
        for attr_name in self.__class__.__dict__:
            #print("check1 ", attr_name, "for", oid, self.__class__ )
            if result is None and attr_name.startswith('SNMP_OID_'):
                print("check2 ", attr_name, "for", oid )
                attr_value = self.__getattribute__(attr_name)
                print(attr_name, "=", attr_value)
                if f and oid == '0':
                    result = attr_value[0]
                    print("get_next0: next oid for {} exists in list - {}".format(oid,attr_value[0]))
                if (attr_value[0] != oid):#attr_value[0].startswith(oid) and
                    result = attr_value[0]
                    print("get_next1: next oid for {} exists in list - {}".format(oid,attr_value[0]))
                if attr_value[0] == oid: #from constants
                    f = True
        #.remove = SnmpPacket(type=SNMP_GETRESPONSE, community=greq.community, id=greq.id)
        #greq.varbinds[oid] = usnmp.ASN1_NULL, None
        print("next:{}->{}".format(oid,result))
        if result != None:
            del gresp.varbinds[oid]
            self._handle_get(result,gresp)
        else:
            gresp.err_status = SNMP_ERR_NOSUCHNAME
            gresp.err_id = 1
            # result = o
        return result



