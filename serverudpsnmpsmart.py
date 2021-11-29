import apcsmartups
from serverudpsnmp import ServerUdpSnmp, const2
from usnmp_codec import ASN1_NULL, ASN1_OID, SNMP_ERR_NOERROR, ASN1_OCTSTR, SNMP_GUAGE, SNMP_TIMETICKS
from time import sleep
import sys

from usnmp_codec import ASN1_INT, SNMP_ERR_NOERROR

SNMP_OID_upsBasicIdentModel                  = const2("1.3.6.1.4.1.318.1.1.1.1.1.1.0")
SNMP_OID_upsAdvIdentFirmwareRevision         = const2("1.3.6.1.4.1.318.1.1.1.1.2.1.0")
SNMP_OID_upsAdvIdentDateOfManufacture        = const2("1.3.6.1.4.1.318.1.1.1.1.2.2.0")
SNMP_OID_upsAdvIdentSerialNumber             = const2("1.3.6.1.4.1.318.1.1.1.1.2.3.0")
SNMP_OID_upsBasicBatteryStatus               = const2("1.3.6.1.4.1.318.1.1.1.2.1.1.0")
SNMP_OID_upsAdvBatteryCapacity               = const2("1.3.6.1.4.1.318.1.1.1.2.2.1.0")
SNMP_OID_upsAdvBatteryTemperature            = const2("1.3.6.1.4.1.318.1.1.1.2.2.2.0")
SNMP_OID_upsAdvBatteryRunTimeRemaining       = const2("1.3.6.1.4.1.318.1.1.1.2.2.3.0")
SNMP_OID_upsAdvBatteryReplaceIndicator       = const2("1.3.6.1.4.1.318.1.1.1.2.2.4.0")
SNMP_OID_upsAdvBatteryActualVoltage          = const2("1.3.6.1.4.1.318.1.1.1.2.2.8.0")
SNMP_OID_upsHighPrecBatteryCapacity          = const2("1.3.6.1.4.1.318.1.1.1.2.3.1.0")
SNMP_OID_upsHighPrecBatteryTemperature       = const2("1.3.6.1.4.1.318.1.1.1.2.3.2.0")
SNMP_OID_upsHighPrecBatteryActualVoltage     = const2("1.3.6.1.4.1.318.1.1.1.2.3.4.0")
SNMP_OID_upsAdvInputLineVoltage              = const2("1.3.6.1.4.1.318.1.1.1.3.2.1.0")
SNMP_OID_upsAdvInputMaxLineVoltage           = const2("1.3.6.1.4.1.318.1.1.1.3.2.2.0")
SNMP_OID_upsAdvInputMinLineVoltage           = const2("1.3.6.1.4.1.318.1.1.1.3.2.3.0")
SNMP_OID_upsAdvInputFrequency                = const2("1.3.6.1.4.1.318.1.1.1.3.2.4.0")
SNMP_OID_upsAdvInputLineFailCause            = const2("1.3.6.1.4.1.318.1.1.1.3.2.5.0")
SNMP_OID_upsHighPrecInputLineVoltage         = const2("1.3.6.1.4.1.318.1.1.1.3.3.1.0")
SNMP_OID_upsHighPrecInputMaxLineVoltage      = const2("1.3.6.1.4.1.318.1.1.1.3.3.2.0")
SNMP_OID_upsHighPrecInputMinLineVoltage      = const2("1.3.6.1.4.1.318.1.1.1.3.3.3.0")
SNMP_OID_upsHighPrecInputFrequency           = const2("1.3.6.1.4.1.318.1.1.1.3.3.4.0")
SNMP_OID_upsBasicOutputStatus                = const2("1.3.6.1.4.1.318.1.1.1.4.1.1.0")
SNMP_OID_upsAdvOutputLoad                    = const2("1.3.6.1.4.1.318.1.1.1.4.2.3.0")
SNMP_OID_upsHighPrecOutputLoad               = const2("1.3.6.1.4.1.318.1.1.1.4.3.3.0")
SNMP_OID_upsAdvConfigRatedOutputVoltage      = const2("1.3.6.1.4.1.318.1.1.1.5.2.1.0")
SNMP_OID_upsAdvConfigHighTransferVolt        = const2("1.3.6.1.4.1.318.1.1.1.5.2.2.0")
SNMP_OID_upsAdvConfigLowTransferVolt         = const2("1.3.6.1.4.1.318.1.1.1.5.2.3.0")
SNMP_OID_upsAdvConfigMinReturnCapacity       = const2("1.3.6.1.4.1.318.1.1.1.5.2.6.0")
SNMP_OID_upsAdvConfigSensitivity             = const2("1.3.6.1.4.1.318.1.1.1.5.2.7.0")
SNMP_OID_upsAdvConfigLowBatteryRunTime       = const2("1.3.6.1.4.1.318.1.1.1.5.2.8.0")
SNMP_OID_upsAdvConfigReturnDelay             = const2("1.3.6.1.4.1.318.1.1.1.5.2.9.0")
SNMP_OID_upsAdvConfigShutoffDelay            = const2("1.3.6.1.4.1.318.1.1.1.5.2.10.0")
SNMP_OID_upsBasicControlConserveBattery      = const2("1.3.6.1.4.1.318.1.1.1.6.1.1.0")
SNMP_OID_upsAdvControlUpsOff                 = const2("1.3.6.1.4.1.318.1.1.1.6.2.1.0")
SNMP_OID_upsAdvControlSimulatePowerFail      = const2("1.3.6.1.4.1.318.1.1.1.6.2.4.0")
SNMP_OID_upsAdvControlFlashAndBeep           = const2("1.3.6.1.4.1.318.1.1.1.6.2.5.0")
SNMP_OID_upsAdvControlTurnOnUPS              = const2("1.3.6.1.4.1.318.1.1.1.6.2.6.0")
SNMP_OID_upsAdvControlBypassSwitch           = const2("1.3.6.1.4.1.318.1.1.1.6.2.7.0")
SNMP_OID_upsAdvTestDiagnostics               = const2("1.3.6.1.4.1.318.1.1.1.7.2.2.0")
SNMP_OID_upsAdvTestRuntimeCalibration        = const2("1.3.6.1.4.1.318.1.1.1.7.2.5.0")
SNMP_OID_upsAdvTestCalibrationResults        = const2("1.3.6.1.4.1.318.1.1.1.7.2.6.0")
SNMP_OID_upsPhaseResetMaxMinValues           = const2("1.3.6.1.4.1.318.1.1.1.9.1.1.0")


class ServerUdpSnmpSmart(ServerUdpSnmp):
    def __init__(self, local_ip='', local_port=161, smart_port='/dev/ttyS0'):
        super().__init__(local_ip, local_port)
        #_SNMP_OIDs = super(ServerUdpSnmpSmart, self).__init__()
        _SNMP_OIDs = super()._SNMP_OIDs
        _SNMP_OIDs[SNMP_OID_upsBasicIdentModel]             = ASN1_OCTSTR, "Smart-UPS APC SC-420"
        _SNMP_OIDs[SNMP_OID_upsAdvIdentFirmwareRevision]    = ASN1_OCTSTR, "411.7.I"
        _SNMP_OIDs[SNMP_OID_upsAdvIdentDateOfManufacture]   = ASN1_OCTSTR, "12/10/07"
        _SNMP_OIDs[SNMP_OID_upsAdvIdentSerialNumber]        = ASN1_OCTSTR, "JS0750000487"
        _SNMP_OIDs[SNMP_OID_upsBasicBatteryStatus]          = ASN1_INT, 2 # INTEGER: batteryNormal(2)
        _SNMP_OIDs[SNMP_OID_upsAdvBatteryCapacity]          = SNMP_GUAGE, 100    #                APC_CMD_BATTLEV
        _SNMP_OIDs[SNMP_OID_upsAdvBatteryTemperature]       = SNMP_GUAGE, 31 #Gauge32: 31
        _SNMP_OIDs[SNMP_OID_upsAdvBatteryRunTimeRemaining]  = SNMP_TIMETICKS, 390000 #Timeticks: (390000) 1:05:00.00
        _SNMP_OIDs[SNMP_OID_upsAdvBatteryReplaceIndicator]  = ASN1_INT, 1 #INTEGER: noBatteryNeedsReplacing(1)
        _SNMP_OIDs[SNMP_OID_upsAdvBatteryActualVoltage]     = ASN1_INT, 54
        _SNMP_OIDs[SNMP_OID_upsHighPrecBatteryCapacity]     = SNMP_GUAGE, 1000
        _SNMP_OIDs[SNMP_OID_upsHighPrecBatteryTemperature]  = SNMP_GUAGE, 310 #Gauge32: 310
        _SNMP_OIDs[SNMP_OID_upsHighPrecBatteryActualVoltage]= ASN1_INT, 540
        _SNMP_OIDs[SNMP_OID_upsAdvInputLineVoltage]         = SNMP_GUAGE, 235
        _SNMP_OIDs[SNMP_OID_upsAdvInputMaxLineVoltage]      = SNMP_GUAGE, 236
        _SNMP_OIDs[SNMP_OID_upsAdvInputMinLineVoltage]      = SNMP_GUAGE, 233
        _SNMP_OIDs[SNMP_OID_upsAdvInputFrequency]           = SNMP_GUAGE, 50
        _SNMP_OIDs[SNMP_OID_upsAdvInputLineFailCause]       = ASN1_INT, 9 #INTEGER: selfTest(9)
        _SNMP_OIDs[SNMP_OID_upsHighPrecInputLineVoltage]    = SNMP_GUAGE, 2361 #Gauge32: 2347
        _SNMP_OIDs[SNMP_OID_upsHighPrecInputMaxLineVoltage] = SNMP_GUAGE, 2376
        _SNMP_OIDs[SNMP_OID_upsHighPrecInputMinLineVoltage] = SNMP_GUAGE, 2332
        _SNMP_OIDs[SNMP_OID_upsHighPrecInputFrequency]      = SNMP_GUAGE, 499
        _SNMP_OIDs[SNMP_OID_upsBasicOutputStatus]           = ASN1_INT, 2 #NTEGER: onLine(2)
        _SNMP_OIDs[SNMP_OID_upsAdvOutputLoad]               = SNMP_GUAGE, 26
        _SNMP_OIDs[SNMP_OID_upsHighPrecOutputLoad]          = SNMP_GUAGE, 260
        _SNMP_OIDs[SNMP_OID_upsAdvConfigRatedOutputVoltage] = ASN1_INT, 230
        _SNMP_OIDs[SNMP_OID_upsAdvConfigHighTransferVolt]   = ASN1_INT, 253
        _SNMP_OIDs[SNMP_OID_upsAdvConfigLowTransferVolt]    = ASN1_INT, 161
        _SNMP_OIDs[SNMP_OID_upsAdvConfigMinReturnCapacity]  = ASN1_INT, 35
        _SNMP_OIDs[SNMP_OID_upsAdvConfigSensitivity]        = ASN1_INT, 0
        _SNMP_OIDs[SNMP_OID_upsAdvConfigLowBatteryRunTime]  = SNMP_TIMETICKS, 90000 #Timeticks: (90000) 0:15:00.00
        _SNMP_OIDs[SNMP_OID_upsAdvConfigReturnDelay]        = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        _SNMP_OIDs[SNMP_OID_upsAdvConfigShutoffDelay]       = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        _SNMP_OIDs[SNMP_OID_upsBasicControlConserveBattery] = ASN1_INT, 1 #NTEGER: noTurnOffUps(1)
        _SNMP_OIDs[SNMP_OID_upsAdvControlUpsOff]            = ASN1_INT, 1 #INTEGER: noTurnUpsOff(1)
        _SNMP_OIDs[SNMP_OID_upsAdvControlSimulatePowerFail] = ASN1_INT, 1 #INTEGER: noSimulatePowerFailure(1)
        _SNMP_OIDs[SNMP_OID_upsAdvControlFlashAndBeep]      = ASN1_INT, 1 #INTEGER: noFlashAndBeep(1)
        _SNMP_OIDs[SNMP_OID_upsAdvControlTurnOnUPS]         = ASN1_INT, 1 # INTEGER: noTurnOnUPS(1)
        _SNMP_OIDs[SNMP_OID_upsAdvControlBypassSwitch]      = ASN1_INT, 1 #INTEGER: noBypassSwitch(1)
        _SNMP_OIDs[SNMP_OID_upsAdvTestDiagnostics]          = ASN1_INT, 1 #INTEGER: noTestDiagnostics(1)
        _SNMP_OIDs[SNMP_OID_upsAdvTestRuntimeCalibration]   = ASN1_INT, 1 #INTEGER: noPerformCalibration(1)
        _SNMP_OIDs[SNMP_OID_upsAdvTestCalibrationResults]   = ASN1_INT, 2 #INTEGER: invalidCalibration(2)
        _SNMP_OIDs[SNMP_OID_upsPhaseResetMaxMinValues]      = ASN1_INT, 1 #INTEGER: none(1)
        self.ups = apcsmartups.ApcSmartUps(smart_port)

    def handle_get(self, oid, community):
        print("handle" , oid)
        if oid == SNMP_OID_upsBasicIdentModel: #calculate response
            res = ASN1_OCTSTR, self.ups.smartpool(self.ups.APC_CMD_UPSMODEL), SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvIdentFirmwareRevision: #calculate response
            res = ASN1_OCTSTR, self.ups.smartpool(self.ups.APC_CMD_REVNO), SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvIdentDateOfManufacture: #calculate response
            res = ASN1_OCTSTR, self.ups.smartpool(self.ups.APC_CMD_MANDAT), SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvIdentSerialNumber: #calculate response
            res = ASN1_OCTSTR, self.ups.smartpool(self.ups.APC_CMD_SERNO), SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsBasicBatteryStatus: #calculate response #unknown = 1, batteryNormal = 2, batteryLow = 3, batteryInFaultCondition = 4
            rstatus = 1
            try:
                status = self.ups.smartpool(self.ups.APC_CMD_STATUS)[0]
                status = int(status.decode(), base=16)
                rstatus = 2
                if status & self.ups.UPS_battlow:
                    rstatus = 3
                if status & self.ups.UPS_replacebatt:
                    rstatus = 4
            except:
                pass
            res = ASN1_INT, rstatus, SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvBatteryCapacity: #calculate response
            res = SNMP_GUAGE, int(self.ups.smartpool(self.ups.APC_CMD_BATTLEV).decode().split(".")[0]), SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvBatteryTemperature: #calculate response
            val = self.ups.smartpool(self.ups.APC_CMD_ITEMP)
            val2 = 0
            if val.isdigit():
                val2 = val.decode()
            res = SNMP_GUAGE, val2, SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvBatteryRunTimeRemaining: #calculate response
            res = SNMP_TIMETICKS, int(self.ups.smartpool(self.ups.APC_CMD_RUNTIM).decode().split(':')[0])*6000, SNMP_ERR_NOERROR
        if oid == SNMP_OID_upsAdvBatteryReplaceIndicator: #calculate response
            status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
            status = int(status.decode(), base=16)
            rstatus = 1
            if status & self.ups.UPS_replacebatt:
                rstatus = 0
            res = ASN1_INT, rstatus, SNMP_ERR_NOERROR
            #print("get:oid {} is temperatureC".format(oid))
        else: #from constants _SNMP_OIDs or SNMP_ERR_NOSUCHNAME
            res = super().handle_get(oid, community)
            print(oid, res)
        return res

