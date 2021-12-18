import apcsmartups
from mibs import SNMP_OID_upsBasicIdentModel, SNMP_OID_upsAdvIdentFirmwareRevision, \
    SNMP_OID_upsAdvBatteryReplaceIndicator, SNMP_OID_upsAdvBatteryRunTimeRemaining, SNMP_OID_upsAdvBatteryTemperature, \
    SNMP_OID_upsAdvBatteryCapacity, SNMP_OID_upsBasicBatteryStatus, SNMP_OID_upsAdvIdentSerialNumber, \
    SNMP_OID_upsAdvIdentDateOfManufacture, SNMP_OID_upsAdvInputFrequency, SNMP_OID_upsAdvInputMinLineVoltage, \
    SNMP_OID_upsAdvInputMaxLineVoltage, SNMP_OID_upsAdvInputLineVoltage, SNMP_OID_upsHighPrecBatteryActualVoltage, \
    SNMP_OID_upsHighPrecBatteryTemperature, SNMP_OID_upsHighPrecBatteryCapacity, SNMP_OID_upsAdvBatteryActualVoltage, \
    SNMP_OID_upsAdvInputLineFailCause, SNMP_OID_upsHighPrecInputLineVoltage, SNMP_OID_upsHighPrecInputMaxLineVoltage, \
    SNMP_OID_upsHighPrecInputMinLineVoltage, SNMP_OID_upsHighPrecInputFrequency, SNMP_OID_upsBasicOutputStatus, \
    SNMP_OID_upsAdvOutputLoad, SNMP_OID_upsHighPrecOutputLoad, SNMP_OID_upsAdvConfigRatedOutputVoltage, \
    SNMP_OID_upsAdvConfigHighTransferVolt, SNMP_OID_upsAdvConfigLowTransferVolt, SNMP_OID_upsAdvConfigMinReturnCapacity, \
    SNMP_OID_upsAdvConfigSensitivity, SNMP_OID_upsAdvConfigLowBatteryRunTime, SNMP_OID_upsAdvConfigReturnDelay, \
    SNMP_OID_upsAdvConfigShutoffDelay, SNMP_OID_upsBasicControlConserveBattery, SNMP_OID_upsAdvControlUpsOff, \
    SNMP_OID_upsAdvControlSimulatePowerFail, SNMP_OID_upsAdvControlFlashAndBeep, SNMP_OID_upsAdvControlTurnOnUPS, \
    SNMP_OID_upsAdvControlBypassSwitch, SNMP_OID_upsAdvTestDiagnostics, SNMP_OID_upsAdvTestRuntimeCalibration, \
    SNMP_OID_upsAdvTestCalibrationResults, SNMP_OID_upsAdvBatteryNominalVoltage, \
    SNMP_OID_upsHighPrecBatteryNominalVoltage, SNMP_OID_upsBasicBatteryLastReplaceDate
from serverudpsnmp import ServerUdpSnmp
# https://sourceforge.net/p/apcupsd/mailman/apcupsd-commits/?viewmonth=200505
# https://networkupstools.org/protocols/apcsmart.html
class ServerUdpSnmpSmart(ServerUdpSnmp):

    def __init__(self, local_ip='', local_port=161, tx=32, rx=33):
        super().__init__(local_ip, local_port)

        self.add_oid(SNMP_OID_upsBasicIdentModel)# "Smart-UPS APC SC-420"
        self.add_oid(SNMP_OID_upsAdvIdentFirmwareRevision)  # "411.7.I"
        self.add_oid(SNMP_OID_upsAdvIdentDateOfManufacture) # "12/10/07"
        self.add_oid(SNMP_OID_upsAdvIdentSerialNumber) # "JS0750000487"
        self.add_oid(SNMP_OID_upsBasicBatteryStatus) # 2 # INTEGER: batteryNormal(2)
        self.add_oid(SNMP_OID_upsBasicBatteryLastReplaceDate) #MM/DD/YY
        self.add_oid(SNMP_OID_upsAdvBatteryCapacity) # 100    #                APC_CMD_BATTLEV
        self.add_oid(SNMP_OID_upsAdvBatteryTemperature) # 31 #Gauge32: 31
        self.add_oid(SNMP_OID_upsAdvBatteryRunTimeRemaining)# 390000 #Timeticks: (390000) 1:05:00.00
        self.add_oid(SNMP_OID_upsAdvBatteryReplaceIndicator)# 1 #INTEGER: noBatteryNeedsReplacing(1)
        self.add_oid(SNMP_OID_upsAdvBatteryNominalVoltage)
        self.add_oid(SNMP_OID_upsAdvBatteryActualVoltage)# 54

        self.add_oid(SNMP_OID_upsHighPrecBatteryCapacity) #     = SNMP_GUAGE, 1000
        self.add_oid(SNMP_OID_upsHighPrecBatteryTemperature) # 310 #Gauge32: 310
        self.add_oid(SNMP_OID_upsHighPrecBatteryNominalVoltage) # 540

        self.add_oid(SNMP_OID_upsHighPrecBatteryActualVoltage) # 540
        self.add_oid(SNMP_OID_upsAdvInputLineVoltage) #         = SNMP_GUAGE, 235, APC_CMD_VLINE
        self.add_oid(SNMP_OID_upsAdvInputMaxLineVoltage) #      = SNMP_GUAGE, 236
        self.add_oid(SNMP_OID_upsAdvInputMinLineVoltage) #      = SNMP_GUAGE, 233
        self.add_oid(SNMP_OID_upsAdvInputFrequency) #           = SNMP_GUAGE, 50
        self.add_oid(SNMP_OID_upsAdvInputLineFailCause) #       = ASN1_INT, 9 #INTEGER: selfTest(9)
        self.add_oid(SNMP_OID_upsHighPrecInputLineVoltage) #    = SNMP_GUAGE, 2361 #Gauge32: 2347
        self.add_oid(SNMP_OID_upsHighPrecInputMaxLineVoltage) # = SNMP_GUAGE, 2376
        self.add_oid(SNMP_OID_upsHighPrecInputMinLineVoltage) # = SNMP_GUAGE, 2332
        self.add_oid(SNMP_OID_upsHighPrecInputFrequency) #      = SNMP_GUAGE, 499
        self.add_oid(SNMP_OID_upsBasicOutputStatus) #           = ASN1_INT, 2 #NTEGER: onLine(2)
        self.add_oid(SNMP_OID_upsAdvOutputLoad) #               = SNMP_GUAGE, 26
        self.add_oid(SNMP_OID_upsHighPrecOutputLoad) #          = SNMP_GUAGE, 260
        self.add_oid(SNMP_OID_upsAdvConfigRatedOutputVoltage) # = ASN1_INT, 230 get/set, Possible values are 100, 120, 208, 220, 225, 230 and 240.
        self.add_oid(SNMP_OID_upsAdvConfigHighTransferVolt) #   = ASN1_INT, 253
        self.add_oid(SNMP_OID_upsAdvConfigLowTransferVolt) #    = ASN1_INT, 161
        self.add_oid(SNMP_OID_upsAdvConfigMinReturnCapacity) #  = ASN1_INT, 35
        self.add_oid(SNMP_OID_upsAdvConfigSensitivity) #        = ASN1_INT, 0 read/write
        self.add_oid(SNMP_OID_upsAdvConfigLowBatteryRunTime) #  = SNMP_TIMETICKS, 90000 #Timeticks: (90000) 0:15:00.00
        self.add_oid(SNMP_OID_upsAdvConfigReturnDelay) #        = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        self.add_oid(SNMP_OID_upsAdvConfigShutoffDelay) #       = SNMP_TIMETICKS, 2000 #Timeticks: (2000) 0:00:20.00
        self.add_oid(SNMP_OID_upsBasicControlConserveBattery) # = ASN1_INT, 1 #NTEGER: noTurnOffUps(1)
        self.add_oid(SNMP_OID_upsAdvControlUpsOff) #            = ASN1_INT, 1 #INTEGER: noTurnUpsOff(1)
        self.add_oid(SNMP_OID_upsAdvControlSimulatePowerFail) # = ASN1_INT, 1 #INTEGER: noSimulatePowerFailure(1)
        self.add_oid(SNMP_OID_upsAdvControlFlashAndBeep) #      = ASN1_INT, 1 #INTEGER: noFlashAndBeep(1)
        self.add_oid(SNMP_OID_upsAdvControlTurnOnUPS) #         = ASN1_INT, 1 # INTEGER: noTurnOnUPS(1)
        self.add_oid(SNMP_OID_upsAdvControlBypassSwitch) #      = ASN1_INT, 1 #INTEGER: noBypassSwitch(1)
        self.add_oid(SNMP_OID_upsAdvTestDiagnostics) #          = ASN1_INT, 1 #INTEGER: noTestDiagnostics(1)
        self.add_oid(SNMP_OID_upsAdvTestRuntimeCalibration) #   = ASN1_INT, 1 #INTEGER: noPerformCalibration(1)
        self.add_oid(SNMP_OID_upsAdvTestCalibrationResults) #   = ASN1_INT, 2 #INTEGER: invalidCalibration(2)
        #self.add_oid(SNMP_OID_upsPhaseResetMaxMinValues) #      = ASN1_INT, 1 #INTEGER: none(1)

        self.ups = apcsmartups.ApcSmartUps(tx=tx, rx=rx)

    def _apc_number_string_to_int(self, val):
        res = int(val.decode().split(".")[0])
        return res
    def _apc_number_string_to_prec_int(self,val):
        res =int(round(10*float(val),1))#parts[0]+parts[1]
        #print(val,'->',res)
        return res

    def handle_get(self, oid, community):
#        print("handle" , oid)
#        print('mem_free',)
        res = None
        if oid == SNMP_OID_upsBasicIdentModel:
            res = self.ups.smartpool(self.ups.APC_CMD_UPSMODEL)
        if oid == SNMP_OID_upsAdvIdentFirmwareRevision:
            res = self.ups.smartpool(self.ups.APC_CMD_REVNO)
        if oid == SNMP_OID_upsAdvIdentDateOfManufacture:
            res = self.ups.smartpool(self.ups.APC_CMD_MANDAT)
        if oid == SNMP_OID_upsAdvIdentSerialNumber:
            res = (self.ups.smartpool(self.ups.APC_CMD_SERNO)+b'        ')[0:8]
        if oid == SNMP_OID_upsBasicBatteryStatus: #calculate response #unknown = 1, batteryNormal = 2, batteryLow = 3, batteryInFaultCondition = 4
            rstatus = 1
            try:
                status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
                status = int(status.decode(), 16)
                rstatus = 2
                if status & self.ups.UPS_battlow:
                    rstatus = 3
                if status & self.ups.UPS_replacebatt:
                    rstatus = 4
            except:
                pass
            res = rstatus
        if oid == SNMP_OID_upsBasicBatteryLastReplaceDate:
            res = self.ups.smartpool(self.ups.APC_CMD_BATTDAT)

        if oid == SNMP_OID_upsAdvBatteryCapacity:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_BATTLEV),)

        if oid == SNMP_OID_upsAdvBatteryTemperature:
            val = self.ups.smartpool(self.ups.APC_CMD_ITEMP)
            val2 = 0
            if val.isdigit():
                val2 = val.decode()
            res = val2

        if oid == SNMP_OID_upsAdvBatteryRunTimeRemaining:
            res = int(self.ups.smartpool(self.ups.APC_CMD_RUNTIM).decode().split(':')[0])*6000

        if oid == SNMP_OID_upsAdvBatteryReplaceIndicator:
            status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
            status = int(status.decode(), 16)
            rstatus = 1
            if status & self.ups.UPS_replacebatt:
                rstatus = 0
            res = rstatus
        if oid==SNMP_OID_upsAdvBatteryNominalVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_NOMBATTV))

        if oid==SNMP_OID_upsAdvBatteryActualVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_VBATT))

        if oid==SNMP_OID_upsHighPrecBatteryCapacity:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_BATTLEV))

        if oid == SNMP_OID_upsHighPrecBatteryTemperature:
            val2 = 0
            val = self.ups.smartpool(self.ups.APC_CMD_ITEMP)
            if val.isdigit():
                val2 = val.decode()
            res = 10*val2
        if oid == SNMP_OID_upsHighPrecBatteryNominalVoltage:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_NOMBATTV))

        if oid == SNMP_OID_upsHighPrecBatteryActualVoltage:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_VBATT))

        if oid == SNMP_OID_upsAdvInputLineVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_VLINE))
        if oid == SNMP_OID_upsAdvInputMaxLineVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_VMAX))
        if oid == SNMP_OID_upsAdvInputMinLineVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_VMIN))
        if oid == SNMP_OID_upsAdvInputFrequency:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_FREQ))
        if oid == SNMP_OID_upsAdvInputLineFailCause:
            res = None #XFER_UNKNOWN;
            status = self.ups.smartpool(self.ups.APC_CMD_WHY_BATT)
            if status == b'N': #XFER_NA;  -> None
                res = None
            if status == b'R': #return XFER_RIPPLE; rateOfVoltageChange(10)"Unacceptable line voltage changes
                res = 10
            if status == b'H': #return XFER_OVERVOLT;-> XFER_OVERVOLT -> highLineVoltage(2)"High line voltage"
                res = 2
            if status == b'L': #return XFER_UNDERVOLT;-> XFER_SELFTEST;-> XFER_UNDERVOLT ->brownout(3),"Low line voltage"
                res = 3
            if status == b'T': #return XFER_NOTCHSPIKE; rateOfVoltageChange(10)"Line voltage notch or spike"
                res = 4
            if status == b'O': #return XFER_NONE; ->XFER_NONE;-> noTransfer(1),"No transfers since turnon"
                res = 1
            if status == b'K': #return XFER_FORCED; ->XFER_NONE;-> noTransfer(1),"Forced by software"
                res =9
            if status == b'S': # return XFER_SELFTEST; -> selfTest(9),"Automatic or explicit self test"
                res = 9
        if oid == SNMP_OID_upsHighPrecInputLineVoltage:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_VLINE))
        if oid == SNMP_OID_upsHighPrecInputMaxLineVoltage:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_VMAX))
        if oid == SNMP_OID_upsHighPrecInputMinLineVoltage:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_VMIN))
        if oid == SNMP_OID_upsHighPrecInputFrequency:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_FREQ))

    #      unknown(1), onLine(2), onBattery(3), onSmartBoost(4), timedSleeping(5), softwareBypass(6), off(7), rebooting(8),
    #      switchedBypass(9), hardwareFailureBypass(10),  sleepingUntilPowerReturn(11),   onSmartTrim(12)
        if oid == SNMP_OID_upsBasicOutputStatus:
            rstatus = 1
            try:
                status = self.ups.smartpool(self.ups.APC_CMD_STATUS)
                status = int(status.decode(),16)
                if status & self.ups.UPS_online:
                    rstatus = 2
                if status & self.ups.UPS_onbatt:
                    rstatus = 3
                if status & self.ups.UPS_boost:
                    rstatus = 4
                if status & self.ups.UPS_trim:
                    rstatus = 12
            except:
                pass
            res = rstatus
        if oid == SNMP_OID_upsAdvOutputLoad:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_LOAD))
        if oid == SNMP_OID_upsHighPrecOutputLoad:
            res = self._apc_number_string_to_prec_int(self.ups.smartpool(self.ups.APC_CMD_LOAD))
        if oid == SNMP_OID_upsAdvConfigRatedOutputVoltage:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_VOUT))
        if oid == SNMP_OID_upsAdvConfigHighTransferVolt:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_HTRANS))
        if oid == SNMP_OID_upsAdvConfigLowTransferVolt:
            res = self._apc_number_string_to_int(self.ups.smartpool(self.ups.APC_CMD_LTRANS))
        if oid == SNMP_OID_upsAdvConfigMinReturnCapacity:
            res = int(self.ups.smartpool(self.ups.APC_CMD_RETPCT))
        if oid == SNMP_OID_upsAdvConfigSensitivity: #0 # 'A': Auto Adjust, 'L': Low, 'M': Medium, 'H': High -> auto(1), low(2), medium(3), high(4)
            val = self.ups.smartpool(self.ups.APC_CMD_SENS)
            if val == b'A':
                res = 1
            if val == b'L':
                res = 2
            if val == b'M':
                res = 3
            if val == b'H':
                res = 4
        if oid == SNMP_OID_upsAdvConfigLowBatteryRunTime:
            res = 6000*int(self.ups.smartpool(self.ups.APC_CMD_DLBATT))

        if oid == SNMP_OID_upsAdvConfigReturnDelay:
            res = 100*int(self.ups.smartpool(self.ups.APC_CMD_DWAKE))

        if oid == SNMP_OID_upsAdvConfigShutoffDelay:
            res = 100*int(self.ups.smartpool(self.ups.APC_CMD_DSHUTD))

        if oid == SNMP_OID_upsBasicControlConserveBattery:
            res = 1 # noTurnOffUps(1) by MIB for read

        if oid == SNMP_OID_upsAdvControlUpsOff:
            res = 1 # noTurnUpsOff(1) by MIB for read

        if oid == SNMP_OID_upsAdvControlSimulatePowerFail:
            res = 1 # noSimulatePowerFailure(1) by MIB for read
        if oid == SNMP_OID_upsAdvControlFlashAndBeep:
            res = 1 # noFlashAndBeep(1) by MIB for read
        if oid == SNMP_OID_upsAdvControlTurnOnUPS:
            res = 1 # noTurnOnUPS(1) by MIB for read
        if oid == SNMP_OID_upsAdvControlBypassSwitch:
            res = 1 # noBypassSwitch(1) by MIB for read
        if oid == SNMP_OID_upsAdvTestDiagnostics:
            res = 1 # noTestDiagnostics(1) by MIB for read
        if oid == SNMP_OID_upsAdvTestRuntimeCalibration:
            res = 1 # noPerformCalibration(1) by MIB for read
        if oid == SNMP_OID_upsAdvTestCalibrationResults:
            res = 2 # invalidCalibration(2) by MIB for read

            #print("get:oid {} is temperatureC".format(oid))
        if res is None: #from constants _SNMP_OIDs or SNMP_ERR_NOSUCHNAME
            res = super().handle_get(oid, community)
            #print(oid, res)
        return res

    def handle_set(self, oid, community, value):

        print('handle_set0',oid, community, value)
        verifed = None
        if community == 'private':
            #print('handle_set1')
            if oid == SNMP_OID_upsBasicBatteryLastReplaceDate:
                #print('handle_set2',oid,value)
                self.ups.change_ups_battery_date(value)
                verifed =  value#self.handle_get(oid,community)
                #print('handle_set3',verifed)
        return verifed