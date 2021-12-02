from usnmp_codec import ASN1_OCTSTR, ASN1_OID, ASN1_INT, SNMP_GUAGE, SNMP_TIMETICKS

try:
    const2('')
except:
    def const2(v):
        return v


SNMP_OID_sysDescr       = const2("1.3.6.1.2.1.1.1.0"), ASN1_OCTSTR
SNMP_OID_sysObjectID    = const2("1.3.6.1.2.1.1.2.0"), ASN1_OID #"1.3.6.1.4.1.318.1.3.1"
SNMP_OID_sysContact     = const2("1.3.6.1.2.1.1.4.0"), ASN1_OCTSTR
SNMP_OID_sysName        = const2("1.3.6.1.2.1.1.5.0"), ASN1_OCTSTR
SNMP_OID_sysLocation    = const2("1.3.6.1.2.1.1.6.0"), ASN1_OCTSTR
SNMP_OID_sysServices    = const2("1.3.6.1.2.1.1.7.0"), ASN1_OCTSTR
SNMP_OID_temperatureC   = const2("1.3.6.1.3.2016.5.1"), ASN1_INT
SNMP_OID_upsBasicIdentModel                  = const2("1.3.6.1.4.1.318.1.1.1.1.1.1.0"),ASN1_OCTSTR # "Smart-UPS APC SC-420"
SNMP_OID_upsAdvIdentFirmwareRevision         = const2("1.3.6.1.4.1.318.1.1.1.1.2.1.0"),ASN1_OCTSTR # "411.7.I"
SNMP_OID_upsAdvIdentDateOfManufacture        = const2("1.3.6.1.4.1.318.1.1.1.1.2.2.0"),ASN1_OCTSTR #, "12/10/07"
SNMP_OID_upsAdvIdentSerialNumber             = const2("1.3.6.1.4.1.318.1.1.1.1.2.3.0"),ASN1_OCTSTR #, "JS0750000487"
SNMP_OID_upsBasicBatteryStatus               = const2("1.3.6.1.4.1.318.1.1.1.2.1.1.0"),ASN1_INT #, 2 # INTEGER: batteryNormal(2)
SNMP_OID_upsAdvBatteryCapacity               = const2("1.3.6.1.4.1.318.1.1.1.2.2.1.0"),SNMP_GUAGE #, 100    #                APC_CMD_BATTLEV
SNMP_OID_upsAdvBatteryTemperature            = const2("1.3.6.1.4.1.318.1.1.1.2.2.2.0"),SNMP_GUAGE #, 31 #Gauge32: 31
SNMP_OID_upsAdvBatteryRunTimeRemaining       = const2("1.3.6.1.4.1.318.1.1.1.2.2.3.0"),SNMP_TIMETICKS #, 390000 #Timeticks: (390000) 1:05:00.00
SNMP_OID_upsAdvBatteryReplaceIndicator       = const2("1.3.6.1.4.1.318.1.1.1.2.2.4.0"),ASN1_INT #, 1 #INTEGER: noBatteryNeedsReplacing(1)
SNMP_OID_upsAdvBatteryNominalVoltage         = const2("1.3.6.1.4.1.318.1.1.1.2.2.7.0"),ASN1_INT
SNMP_OID_upsAdvBatteryActualVoltage          = const2("1.3.6.1.4.1.318.1.1.1.2.2.8.0"),ASN1_INT #, 54
SNMP_OID_upsHighPrecBatteryCapacity          = const2("1.3.6.1.4.1.318.1.1.1.2.3.1.0"),SNMP_GUAGE #, 1000
SNMP_OID_upsHighPrecBatteryTemperature       = const2("1.3.6.1.4.1.318.1.1.1.2.3.2.0"),SNMP_GUAGE #, 310 #Gauge32: 310
SNMP_OID_upsHighPrecBatteryNominalVoltage    = const2("1.3.6.1.4.1.318.1.1.1.2.3.3.0"),ASN1_INT
SNMP_OID_upsHighPrecBatteryActualVoltage     = const2("1.3.6.1.4.1.318.1.1.1.2.3.4.0"),ASN1_INT #, 540
SNMP_OID_upsAdvInputLineVoltage              = const2("1.3.6.1.4.1.318.1.1.1.3.2.1.0"),SNMP_GUAGE #, 235
SNMP_OID_upsAdvInputMaxLineVoltage           = const2("1.3.6.1.4.1.318.1.1.1.3.2.2.0"),SNMP_GUAGE #, 236
SNMP_OID_upsAdvInputMinLineVoltage           = const2("1.3.6.1.4.1.318.1.1.1.3.2.3.0"),SNMP_GUAGE #, 233
SNMP_OID_upsAdvInputFrequency                = const2("1.3.6.1.4.1.318.1.1.1.3.2.4.0"),SNMP_GUAGE #, 50
SNMP_OID_upsAdvInputLineFailCause            = const2("1.3.6.1.4.1.318.1.1.1.3.2.5.0"),ASN1_INT #, 9 #INTEGER: selfTest(9)
SNMP_OID_upsHighPrecInputLineVoltage         = const2("1.3.6.1.4.1.318.1.1.1.3.3.1.0"),SNMP_GUAGE #, 2361 #Gauge32: 2347
SNMP_OID_upsHighPrecInputMaxLineVoltage      = const2("1.3.6.1.4.1.318.1.1.1.3.3.2.0"),SNMP_GUAGE #, 2376
SNMP_OID_upsHighPrecInputMinLineVoltage      = const2("1.3.6.1.4.1.318.1.1.1.3.3.3.0"),SNMP_GUAGE #, 2332
SNMP_OID_upsHighPrecInputFrequency           = const2("1.3.6.1.4.1.318.1.1.1.3.3.4.0"),SNMP_GUAGE #, 499
SNMP_OID_upsBasicOutputStatus                = const2("1.3.6.1.4.1.318.1.1.1.4.1.1.0"),ASN1_INT #, 2 #NTEGER: onLine(2)
SNMP_OID_upsAdvOutputLoad                    = const2("1.3.6.1.4.1.318.1.1.1.4.2.3.0"),SNMP_GUAGE #, 26
SNMP_OID_upsHighPrecOutputLoad               = const2("1.3.6.1.4.1.318.1.1.1.4.3.3.0"),SNMP_GUAGE #, 260
SNMP_OID_upsAdvConfigRatedOutputVoltage      = const2("1.3.6.1.4.1.318.1.1.1.5.2.1.0"),ASN1_INT #, 230 read/write
SNMP_OID_upsAdvConfigHighTransferVolt        = const2("1.3.6.1.4.1.318.1.1.1.5.2.2.0"),ASN1_INT #, 253 read/write
SNMP_OID_upsAdvConfigLowTransferVolt         = const2("1.3.6.1.4.1.318.1.1.1.5.2.3.0"),ASN1_INT #, 161 read/write
SNMP_OID_upsAdvConfigMinReturnCapacity       = const2("1.3.6.1.4.1.318.1.1.1.5.2.6.0"),ASN1_INT #, 35 read/write
SNMP_OID_upsAdvConfigSensitivity             = const2("1.3.6.1.4.1.318.1.1.1.5.2.7.0"),ASN1_INT #, 0 read/write auto(1),low(2),medium(3),high(4)
SNMP_OID_upsAdvConfigLowBatteryRunTime       = const2("1.3.6.1.4.1.318.1.1.1.5.2.8.0"),SNMP_TIMETICKS #,  90000 #Timeticks: (90000) 0:15:00.00
SNMP_OID_upsAdvConfigReturnDelay             = const2("1.3.6.1.4.1.318.1.1.1.5.2.9.0"),SNMP_TIMETICKS #, 2000 #Timeticks: (2000) 0:00:20.00
SNMP_OID_upsAdvConfigShutoffDelay            = const2("1.3.6.1.4.1.318.1.1.1.5.2.10.0"),SNMP_TIMETICKS #, 2000 #Timeticks: (2000) 0:00:20.00
SNMP_OID_upsBasicControlConserveBattery      = const2("1.3.6.1.4.1.318.1.1.1.6.1.1.0"),ASN1_INT #, 1 #NTEGER: noTurnOffUps(1)
SNMP_OID_upsAdvControlUpsOff                 = const2("1.3.6.1.4.1.318.1.1.1.6.2.1.0"),ASN1_INT #, 1 #INTEGER: noTurnUpsOff(1)
SNMP_OID_upsAdvControlSimulatePowerFail      = const2("1.3.6.1.4.1.318.1.1.1.6.2.4.0"),ASN1_INT #, 1 #INTEGER: noSimulatePowerFailure(1)
SNMP_OID_upsAdvControlFlashAndBeep           = const2("1.3.6.1.4.1.318.1.1.1.6.2.5.0"),ASN1_INT #, 1 #INTEGER: noFlashAndBeep(1)
SNMP_OID_upsAdvControlTurnOnUPS              = const2("1.3.6.1.4.1.318.1.1.1.6.2.6.0"),ASN1_INT #, 1 # INTEGER: noTurnOnUPS(1)
SNMP_OID_upsAdvControlBypassSwitch           = const2("1.3.6.1.4.1.318.1.1.1.6.2.7.0"),ASN1_INT #, 1 #INTEGER: noBypassSwitch(1) #noBypassSwitch (1),switchToBypass (2),switchOutOfBypass(3)
SNMP_OID_upsAdvTestDiagnostics               = const2("1.3.6.1.4.1.318.1.1.1.7.2.2.0"),ASN1_INT #, 1 #INTEGER: noTestDiagnostics(1)
SNMP_OID_upsAdvTestRuntimeCalibration        = const2("1.3.6.1.4.1.318.1.1.1.7.2.5.0"),ASN1_INT #, 1 #INTEGER: noPerformCalibration(1)
SNMP_OID_upsAdvTestCalibrationResults        = const2("1.3.6.1.4.1.318.1.1.1.7.2.6.0"),ASN1_INT #, 2 #INTEGER: invalidCalibration(2)
SNMP_OID_upsPhaseResetMaxMinValues           = const2("1.3.6.1.4.1.318.1.1.1.9.1.1.0"),ASN1_INT #, 1 #INTEGER: none(1)


