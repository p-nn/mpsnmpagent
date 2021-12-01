import apcsmartups
from mibs import SNMP_OID_upsBasicIdentModel, SNMP_OID_upsAdvIdentFirmwareRevision, \
    SNMP_OID_upsAdvBatteryReplaceIndicator, SNMP_OID_upsAdvBatteryRunTimeRemaining, SNMP_OID_upsAdvBatteryTemperature, \
    SNMP_OID_upsAdvBatteryCapacity, SNMP_OID_upsBasicBatteryStatus, SNMP_OID_upsAdvIdentSerialNumber, \
    SNMP_OID_upsAdvIdentDateOfManufacture
#from serverudpsnmp import ServerUdpSnmp, const2
from serverudpsnmp2 import ServerUdpSnmp2
from usnmp_codec import ASN1_NULL, ASN1_OID, SNMP_ERR_NOERROR, ASN1_OCTSTR, SNMP_GUAGE, SNMP_TIMETICKS
from time import sleep
import sys

from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR


class ServerUdpSnmpSmart(ServerUdpSnmp2):

    def __init__(self, local_ip='', local_port=161, smart_port='/dev/ttyS0'):
        super().__init__(local_ip, local_port)
        #_SNMP_OIDs = super(ServerUdpSnmpSmart, self).__init__()
        self.add_oid(SNMP_OID_upsBasicIdentModel)# "Smart-UPS APC SC-420"
        self.add_oid(SNMP_OID_upsAdvIdentFirmwareRevision)  # "411.7.I"
        self.add_oid(SNMP_OID_upsAdvIdentDateOfManufacture) # "12/10/07"
        self.add_oid(SNMP_OID_upsAdvIdentSerialNumber) # "JS0750000487"
        self.add_oid(SNMP_OID_upsBasicBatteryStatus) # 2 # INTEGER: batteryNormal(2)
        self.add_oid(SNMP_OID_upsAdvBatteryCapacity) # 100    #                APC_CMD_BATTLEV
        self.add_oid(SNMP_OID_upsAdvBatteryTemperature) # 31 #Gauge32: 31
        self.add_oid(SNMP_OID_upsAdvBatteryRunTimeRemaining)# 390000 #Timeticks: (390000) 1:05:00.00
        self.add_oid(SNMP_OID_upsAdvBatteryReplaceIndicator)# 1 #INTEGER: noBatteryNeedsReplacing(1)
        
        #self.add_oid(SNMP_OID_upsAdvBatteryActualVoltage)# 54
        #self.add_oid(SNMP_OID_upsHighPrecBatteryCapacity) #     = SNMP_GUAGE, 1000
        #self.add_oid(SNMP_OID_upsHighPrecBatteryTemperature) # 310 #Gauge32: 310
        #self.add_oid(SNMP_OID_upsHighPrecBatteryActualVoltage) # 540
        #self.add_oid(SNMP_OID_upsAdvInputLineVoltage) #         = SNMP_GUAGE, 235
        #self.add_oid(SNMP_OID_upsAdvInputMaxLineVoltage) #      = SNMP_GUAGE, 236
        #self.add_oid(SNMP_OID_upsAdvInputMinLineVoltage) #      = SNMP_GUAGE, 233
        #self.add_oid(SNMP_OID_upsAdvInputFrequency) #           = SNMP_GUAGE, 50
        #self.add_oid(SNMP_OID_upsAdvInputLineFailCause) #       = ASN1_INT, 9 #INTEGER: selfTest(9)
        #self.add_oid(SNMP_OID_upsHighPrecInputLineVoltage) #    = SNMP_GUAGE, 2361 #Gauge32: 2347
        #self.add_oid(SNMP_OID_upsHighPrecInputMaxLineVoltage) # = SNMP_GUAGE, 2376
        #self.add_oid(SNMP_OID_upsHighPrecInputMinLineVoltage) # = SNMP_GUAGE, 2332
        #self.add_oid(SNMP_OID_upsHighPrecInputFrequency) #      = SNMP_GUAGE, 499
        #self.add_oid(SNMP_OID_upsBasicOutputStatus) #           = ASN1_INT, 2 #NTEGER: onLine(2)
        #self.add_oid(SNMP_OID_upsAdvOutputLoad) #               = SNMP_GUAGE, 26
        #self.add_oid(SNMP_OID_upsHighPrecOutputLoad) #          = SNMP_GUAGE, 260
        #self.add_oid(SNMP_OID_upsAdvConfigRatedOutputVoltage) # = ASN1_INT, 230
        #self.add_oid(SNMP_OID_upsAdvConfigHighTransferVolt) #   = ASN1_INT, 253
        #self.add_oid(SNMP_OID_upsAdvConfigLowTransferVolt) #    = ASN1_INT, 161
        #self.add_oid(SNMP_OID_upsAdvConfigMinReturnCapacity) #  = ASN1_INT, 35
        #self.add_oid(SNMP_OID_upsAdvConfigSensitivity) #        = ASN1_INT, 0
        #self.add_oid(SNMP_OID_upsAdvConfigLowBatteryRunTime) #  = SNMP_TIMETICKS, 90000 #Timeticks: (90000) 0:15:00.00
        #self.add_oid(SNMP_OID_upsAdvConfigReturnDelay) #        = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        #self.add_oid(SNMP_OID_upsAdvConfigShutoffDelay) #       = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        #self.add_oid(SNMP_OID_upsBasicControlConserveBattery) # = ASN1_INT, 1 #NTEGER: noTurnOffUps(1)
        #self.add_oid(SNMP_OID_upsAdvControlUpsOff) #            = ASN1_INT, 1 #INTEGER: noTurnUpsOff(1)
        #self.add_oid(SNMP_OID_upsAdvControlSimulatePowerFail) # = ASN1_INT, 1 #INTEGER: noSimulatePowerFailure(1)
        #self.add_oid(SNMP_OID_upsAdvControlFlashAndBeep) #      = ASN1_INT, 1 #INTEGER: noFlashAndBeep(1)
        #self.add_oid(SNMP_OID_upsAdvControlTurnOnUPS) #         = ASN1_INT, 1 # INTEGER: noTurnOnUPS(1)
        #self.add_oid(SNMP_OID_upsAdvControlBypassSwitch) #      = ASN1_INT, 1 #INTEGER: noBypassSwitch(1)
        #self.add_oid(SNMP_OID_upsAdvTestDiagnostics) #          = ASN1_INT, 1 #INTEGER: noTestDiagnostics(1)
        #self.add_oid(SNMP_OID_upsAdvTestRuntimeCalibration) #   = ASN1_INT, 1 #INTEGER: noPerformCalibration(1)
        #self.add_oid(SNMP_OID_upsAdvTestCalibrationResults) #   = ASN1_INT, 2 #INTEGER: invalidCalibration(2)
        #self.add_oid(SNMP_OID_upsPhaseResetMaxMinValues) #      = ASN1_INT, 1 #INTEGER: none(1)

        self.ups = apcsmartups.ApcSmartUps(smart_port)

    def handle_get(self, oid, community):
        print("handle" , oid)
        if oid == SNMP_OID_upsBasicIdentModel[0]: #calculate response
            res = self.ups.smartpool(self.ups.APC_CMD_UPSMODEL)
        if oid == SNMP_OID_upsAdvIdentFirmwareRevision[0]: #calculate response
            res = self.ups.smartpool(self.ups.APC_CMD_REVNO)
        if oid == SNMP_OID_upsAdvIdentDateOfManufacture[0]: #calculate response
            res = self.ups.smartpool(self.ups.APC_CMD_MANDAT)
        if oid == SNMP_OID_upsAdvIdentSerialNumber[0]: #calculate response
            res = self.ups.smartpool(self.ups.APC_CMD_SERNO).rjust(8)[0:8]
        if oid == SNMP_OID_upsBasicBatteryStatus[0]: #calculate response #unknown = 1, batteryNormal = 2, batteryLow = 3, batteryInFaultCondition = 4
            rstatus = 1
            try:
                status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
                status = int(status.decode(), base=16)
                rstatus = 2
                if status & self.ups.UPS_battlow:
                    rstatus = 3
                if status & self.ups.UPS_replacebatt:
                    rstatus = 4
            except:
                pass
            res = rstatus
        if oid == SNMP_OID_upsAdvBatteryCapacity[0]: #calculate response
            res = int(self.ups.smartpool(self.ups.APC_CMD_BATTLEV).decode().split(".")[0])
        if oid == SNMP_OID_upsAdvBatteryTemperature[0]: #calculate response
            val = self.ups.smartpool(self.ups.APC_CMD_ITEMP)
            val2 = 0
            if val.isdigit():
                val2 = val.decode()
            res = val2
        if oid == SNMP_OID_upsAdvBatteryRunTimeRemaining[0]: #calculate response
            res = int(self.ups.smartpool(self.ups.APC_CMD_RUNTIM).decode().split(':')[0])*6000
        if oid == SNMP_OID_upsAdvBatteryReplaceIndicator[0]: #calculate response
            status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
            status = int(status.decode(), base=16)
            rstatus = 1
            if status & self.ups.UPS_replacebatt:
                rstatus = 0
            res = rstatus
            #print("get:oid {} is temperatureC".format(oid))
        if res is None: #from constants _SNMP_OIDs or SNMP_ERR_NOSUCHNAME
            res = super().handle_get(oid, community)
            print(oid, res)
        return res

