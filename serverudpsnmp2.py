import collections
import time
from serverudp import ServerUdp
from usnmp import SNMP_GETREQUEST, SNMP_GETNEXTREQUEST, SNMP_SETREQUEST, SNMP_GETRESPONSE, SnmpPacket, ASN1_OCTSTR, SNMP_ERR_NOSUCHNAME
from usnmp_codec import ASN1_NULL, ASN1_OID, SNMP_ERR_NOERROR, SNMP_ERR_BADVALUE

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
    #const starts with 'SNMP_OID_' is tuple, "sysDescr"
    #    ASN.1 sequence and SNMP derivatives
    #    #IMPORTANT manual order need for getnext over reflection
    OIDS = collections.deque()# OrderedDict() #list of oids from mibs
#    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0"),ASN1_OCTSTR
#    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0"),ASN1_OID
    def add_oid(self, const_from_mibs):
        self.OIDS.append(const_from_mibs)


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
                self._handle_get_next(oid,gresp)
            if greq.type==SNMP_SETREQUEST:
                self._handle_set(oid,greq, gresp)


        print("Message from Client:{}".format(greq.type))
        print("Client IP Address:{}".format(address))
        # Sending a reply to client

        print("sending:{}".format(gresp))
        for o in gresp.varbinds:
            print("sending varbinds:", o, gresp.varbinds[o])
        bytesToSend = gresp.tobytes()
        self.socket.sendto(bytesToSend, address)
        #print(time.time())
        return True

    def handle_get(self, oid, community):
        return None

    def _handle_get(self, oid, gresp):#usnmp.SNMP_GETREQUEST
        res = None
        for attr in self.OIDS:
            #print("handle_get_check: ",attr_name)
            if res is None:
                if attr[0] == oid: #from constants
                    print("handle_get: ",attr[0], "=", attr[1])
                    #res =, self.NVS[attr_value[0]], SNMP_ERR_NOERROR
                    res = attr[1], self.handle_get(oid, gresp.community), SNMP_ERR_NOERROR # break
        if res == None:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)
        gresp.varbinds[oid] = res[0], res[1]
        gresp.err_status = res[2]

    def handle_set(self, oid, community, value):
        print(oid, community, value)
        value_verifed = value
        return value_verifed

    def _handle_set(self, oid, greq, gresp):
        print("set:{}".format(oid),greq)
        vtype = greq.varbinds[oid][0]
        value = greq.varbinds[oid][1]
        res = None
        for attr in self.OIDS:
            if attr[0] == oid:
               #print("types:",attr_value[1],vtype)
                if attr[1] == vtype:
                    res = (vtype, self.handle_set(oid,gresp.community,greq.varbinds[oid][1]), SNMP_ERR_NOERROR)
                else:
                    #print("wrong type:",attr_value[0],"<>",vtype),
                    res = (vtype, value, SNMP_ERR_BADVALUE)
        if res is None:
            res = (ASN1_NULL, None, SNMP_ERR_NOSUCHNAME)

        gresp.varbinds[oid] = res[0], res[1]
        gresp.err_status = res[2]


    def _handle_get_next(self,oid, gresp):
        f = oid=="0"
        #o = None
        result = None
        #    if oid in _SNMP_OIDs.keys():
        print("get_next: oid {} check in attributes".format(oid),"reverse=")
        for attr in self.OIDS:
            #print("check1 ", attr_name, "for", oid, self.__class__ )
            if result is None:
                if f or oid == '0':
                    result = attr[0]
                if attr[0].startswith(oid) and(attr[0] != oid):#
                    result = attr[0]
                if attr[0] == oid: #from constants
                    f = True
        print("next:{}->{}".format(oid,result))
        if result != None:
            self._handle_get(result,gresp)
        else:
            gresp.err_status = SNMP_ERR_NOSUCHNAME
            gresp.err_id = 1
            # result = o
        return result



