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

#    SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0"),ASN1_OCTSTR
#    SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0"),ASN1_OID
    reverse_order = False # micropython have reversed __dict__
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
        for attr_name in self.__class__.__dict__:
            #print("handle_get_check: ",attr_name)
            if res is None and attr_name.startswith('SNMP_OID_'):
                attr_value = self.__class__.__dict__[attr_name]
                if attr_value[0] == oid: #from constants
                    print("handle_get: ",attr_name, "=", attr_value)
                    #res =, self.NVS[attr_value[0]], SNMP_ERR_NOERROR
                    res = attr_value[1], self.handle_get(oid, gresp.community), SNMP_ERR_NOERROR # break
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
        for attr_name in self.__class__.__dict__:
            if attr_name.startswith('SNMP_OID_'):
                attr_value = self.__class__.__dict__[attr_name]
                if attr_value[0] == oid:
                    #print("types:",attr_value[1],vtype)
                    if attr_value[1] == vtype:
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
        print("get_next: oid {} check in attributes".format(oid),"reverse=",self.reverse_order)
        dict = self.__class__.__dict__
        if self.reverse_order:
            dict = dict.__reversed__()
        for attr_name in dict:
            #print("check1 ", attr_name, "for", oid, self.__class__ )
            if result is None and attr_name.startswith('SNMP_OID_'):
                attr_value = self.__class__.__dict__[attr_name]
                if f or oid == '0':
                    result = attr_value[0]
                if attr_value[0].startswith(oid) and(attr_value[0] != oid):#
                    result = attr_value[0]
                if attr_value[0] == oid: #from constants
                    f = True
        print("next:{}->{}".format(oid,result))
        if result != None:
            self._handle_get(result,gresp)
        else:
            gresp.err_status = SNMP_ERR_NOSUCHNAME
            gresp.err_id = 1
            # result = o
        return result



