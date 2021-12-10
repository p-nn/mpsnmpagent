import time
from machine import UART


# https://sourceforge.net/p/apcupsd/mailman/apcupsd-commits/?viewmonth=200505
# https://networkupstools.org/protocols/apcsmart.html
class ApcSmartUps:

    SMART_DELAY_COMM_READ = 0.1 #0.3     #delay sec
    SMART_DELAY_COMM_WRITE = 1 #1      #delay sec
    # bit values for APC UPS Status Byte (ups->Status)
    UPS_calibration = 0x00000001
    UPS_trim = 0x00000002
    UPS_boost = 0x00000004
    UPS_online = 0x00000008
    UPS_onbatt = 0x00000010
    UPS_overload = 0x00000020
    UPS_battlow = 0x00000040
    UPS_replacebatt = 0x00000080

    # /*
    # * APC_CMD_ is the command code sent to UPS for APC Smart UPSes
    # *
    # * NOTE: the APC_CMD_s are never used in the actual code,
    # * except to initialize the UPS_Cmd[] structure. This way,
    # * we will be able to support other UPSes later. The actual
    # * command is obtained by reference to UPS_Cmd[CI_xxx]
    # */

    APC_CMD_UPSMODEL = b'\x01' #bytes.fromhex('01')  # Model number
    APC_CMD_OLDFWREV = b'V'  # status function
    APC_CMD_STATUS = b'Q'  # line quality status
    APC_CMD_LQUAL = b'9'  # line quality status
    APC_CMD_WHY_BATT = b'G'  # why transferred to battery
    APC_CMD_ST_STAT = b'X'  # self test stat
    APC_CMD_VLINE = b'L'  # line voltage
    APC_CMD_VMAX = b'M'  # max voltage
    APC_CMD_VMIN = b'N'  # min line voltage
    APC_CMD_VOUT = b'O'  # Output voltage
    APC_CMD_BATTLEV = b'f'  # Battery level percentage
    APC_CMD_VBATT = b'B'  # Battery voltage
    APC_CMD_LOAD = b'P'  # UPS Load
    APC_CMD_FREQ = b'F'  # Line Frequency
    APC_CMD_RUNTIM = b'j'  # Est. Runtime left */
    APC_CMD_ITEMP = b'C'  # Internal UPS temperature
    APC_CMD_DIPSW = b'7'  # Dip switch settings
    APC_CMD_SENS = b's'  # Sensitivity 'A': Auto Adjust, 'L': Low, 'M': Medium, 'H': High
    APC_CMD_DWAKE = b'r'  # Wakeup delay
    APC_CMD_DSHUTD = b'p'  # Shutdown delay
    APC_CMD_LTRANS = b'l'  # Low transfer voltage
    APC_CMD_HTRANS = b'u'  # High transfer voltage
    APC_CMD_RETPCT = b'e'  # Return percent threshhold
    APC_CMD_DALARM = b'k'  # Alarm delay
    APC_CMD_DLBATT = b'q'  # low battery warning, mins
    APC_CMD_IDEN = b'c'  # UPS Identification (name)
    APC_CMD_STESTI = b'E'  # Self test interval
    APC_CMD_MANDAT = b'm'  # Manufacture date
    APC_CMD_SERNO = b'n'  # serial number
    APC_CMD_BATTDAT = b'x'  # BatteryLastReplaceDate.0 = STRING8: "03/07/19
    APC_CMD_NOMBATTV = b'g'  # Nominal battery voltage
    APC_CMD_HUMID = b'h'  # UPS Humidity percentage
    APC_CMD_REVNO = b'b'  # Firmware revision
    APC_CMD_REG1 = b'~'
    APC_CMD_REG2 = b'\''
    APC_CMD_REG3 = b'8'
    APC_CMD_EXTBATTS = b'>'  # Number of external batteries
    APC_CMD_ATEMP = b't'  # Ambient temp
    APC_CMD_NOMOUTV = b'o'  # Nominal output voltage
    APC_CMD_BADBATTS = b'<'  # Number of bad battery packs
    APC_CMD_EPROM = b'\x1a' #bytes.fromhex('1a')  # Valid eprom values
    APC_CMD_ST_TIME = b'd'  # hours since last self test
    APC_CMD_CYCLE_EPROM = b'-'  # Cycle programmable EPROM values
    APC_CMD_UPS_CAPS = b'a'  # Get UPS capabilities (command) string
    GO_ON_BATT = b'W'
    GO_ON_LINE = b'X'
    LIGHTS_TEST = b'A'
    FAILURE_TEST = b'U'

    # /*
    # * Future additions for contolled discharing of batteries
    # * extend lifetimes.
    # */

    DISCHARGE = b'D'
    CHARGE_LIM = 25

    UPS_ENABLED = b'?'
    UPS_ON_BATT = b'!'
    UPS_ON_LINE = b'$'
    UPS_REPLACE_BATTERY = b'#'
    BATT_LOW = b'%'
    BATT_OK = b'+'
    UPS_EPROM_CHANGE = b'|'
    UPS_TRAILOR = b':'
    UPS_LF = b'\n'
    UPS_CR = b'\r'

    SUCCESS = 0  # Function successfull */
    FAILURE = 1  # Function failure */

    alert = b' '

    def __init__(self, tx=32, rx=33):
        self.online = False
        self.stat = ''
        try:
#            self.serialport = serial.Serial(port=port, baudrate=2400, parity=serial.PARITY_NONE, stopbits=1, xonxoff=0,
#                                            bytesize=8)
            self.serialport = UART(1, baudrate=2400, bits=8, parity=None, stop=1, tx=tx, rx=rx,
                                   timeout=1000, timeout_char=1000)
            self.UPSlinkCheck()
            # self.stat = self.smartpool(APC_CMD_UPS_CAPS)
        except:
            pass

    def UPSlinkCheck(self):
        self.online = False
        self.serialport.write(b'Y')  # write a string
        time.sleep(self.SMART_DELAY_COMM_READ)
        r = self.serialport.readline()
        if r == b'SM\r\n':
            self.online = True
        return self.online

    def close(self):
        self.serialport.deinit()

    def _extract_flags(self, response):
        # print(response[0:1])
        n = 0
        for i in range(len(response) - 1):
            if response[i:i + 1] in (
                    self.UPS_ON_BATT, self.UPS_ON_LINE, self.UPS_REPLACE_BATTERY, self.UPS_ENABLED,
                    self.UPS_REPLACE_BATTERY,
                    self.BATT_LOW, self.BATT_OK, self.UPS_EPROM_CHANGE):
                # print('=',response[i:i+1])
                n = i + 1
                break
        return response[n:], response[:n]

    def smartpool(self, cmd):  # read data without \r\n
        #self.serialport.timeout = 1
        self.serialport.write(cmd)
        print(cmd)
        time.sleep(self.SMART_DELAY_COMM_READ) #0.3            need > 0.2
        stat = self.serialport.readline()
        stat2, self.alert = self._extract_flags(stat)
        if len(self.alert) > 0:
            print('##############################################################################', self.alert)
        print('smartpool:', cmd, '->', stat, '->', stat2)

        return stat2[:-2]  # drop final \r\n

    def change_ups_eeprom_item(self, cmd, bytes):
        #self.serialport.timeout = 4
        #self.serialport.timeout = 4

        self.serialport.write(cmd)
        time.sleep(self.SMART_DELAY_COMM_READ)

        oldname = self.serialport.readline()

        print('set new name:  {}'.format(bytes))
        print("old name     : {}".format(oldname))

        #self.serialport.write_timeout = 4
        self.serialport.write(self.APC_CMD_CYCLE_EPROM)

        time.sleep(self.SMART_DELAY_COMM_WRITE)
        arr = bytearray(bytes)
        for i in range(len(bytes)):
            self.serialport.write(arr[i:i + 1])
            print('write to ups {}'.format(arr[i:i + 1]))
            time.sleep(self.SMART_DELAY_COMM_WRITE)
        response = self.serialport.readline()
        response, self.alert = self._extract_flags(response)
        print("Response: {}".format(response))
        if response != b'OK\r\n':
            print("\nError changing UPS name\n")
        #self.serialport.write_timeout = 1
        #self.serialport.timeout = 1
        #self.serialport.write(cmd)

        return self.smartpool(cmd)

    def change_ups_name2(self, newname):
        newname = (newname.encode()+b'        ')[0:8]
        return self.change_ups_eeprom_item(self.APC_CMD_IDEN, newname)

    def change_ups_battery_date(self, newdate):
        # print(newdate)
        # month = int(newdate[0:2])
        # day = int(newdate[3:5])
        # year = int(newdate[6:8])
        # res = month>0 & month<13 & day > 0 & day<32
        # print(str(newdate[0:2]),str(newdate[3:5]),str(newdate[6:8]),month,day,year,res)
        newdate = (newdate.encode()+b'        ')[0:8]
        #            res = True
        return self.change_ups_eeprom_item(self.APC_CMD_BATTDAT, newdate)

    def change_ups_name(self, newname):
        #self.serialport.timeout = 4
        newname = (newname.encode()+b'        ')[0:8]

        self.serialport.write(self.APC_CMD_IDEN)
        time.sleep(self.SMART_DELAY_COMM_READ)
        oldname = self.serialport.readline()

        print('set new name: {}'.format(newname))
        print("APC_CMD_IDEN: {}".format(oldname))

        #self.serialport.write_timeout = 4
        self.serialport.write(self.APC_CMD_CYCLE_EPROM)
        time.sleep(self.SMART_DELAY_COMM_WRITE)
        arr = bytearray(newname)
        for i in range(8):
            self.serialport.write(arr[i:i + 1])
            print('write to ups {}'.format(arr[i:i + 1]))
            time.sleep(self.SMART_DELAY_COMM_WRITE)
        response = self.serialport.readline()
        print("Response: {}".format(response))
        if response == b'OK' or response == b'|OK':
            print("\nError changing UPS name\n")
        #self.serialport.write_timeout = 1
        #self.serialport.timeout = 1
        self.serialport.write(self.APC_CMD_IDEN)
        time.sleep(self.SMART_DELAY_COMM_READ)
        return self.serialport.readline()

    #    def read_volatile_data():

    def testUps(self):
        print(self.serialport)  # check which port was really used
        print("ups online: {}".format(self.online))
        if self.online:
            print("APC_CMD_UPSMODEL: {}".format(self.smartpool(self.APC_CMD_UPSMODEL)))
            print("APC_CMD_SERNO: {}".format(self.smartpool(self.APC_CMD_SERNO)))
            # print("APC_CMD_EPROM: {}".format(ups.smartpool(ups.APC_CMD_EPROM)))
            print("APC_CMD_STATUS: {}".format(self.smartpool(self.APC_CMD_STATUS)))
            print("APC_CMD_VLINE: {}".format(self.smartpool(self.APC_CMD_VLINE)))
            print("APC_CMD_LOAD: {}".format(self.smartpool(self.APC_CMD_LOAD)))
            print("APC_CMD_BATTLEV: {}".format(self.smartpool(self.APC_CMD_BATTLEV)))
            print("APC_CMD_RUNTIM: {}".format(self.smartpool(self.APC_CMD_RUNTIM)))
            print("APC_CMD_ITEMP: {}".format(self.smartpool(self.APC_CMD_ITEMP)))
            print("APC_CMD_BATTDAT: {}".format(self.smartpool(self.APC_CMD_BATTDAT)))
            print("APC_CMD_DALARM: {}".format(self.smartpool(self.APC_CMD_DALARM)))
            print("APC_CMD_DLBATT: {}".format(self.smartpool(self.APC_CMD_DLBATT)))
            print("APC_CMD_DWAKE: {}".format(self.smartpool(self.APC_CMD_DWAKE)))
            print("APC_CMD_DSHUTD: {}".format(self.smartpool(self.APC_CMD_DSHUTD)))
            print("APC_CMD_NOMOUTV: {}".format(self.smartpool(self.APC_CMD_NOMOUTV)))
            print("APC_CMD_NOMBATTV: {}".format(self.smartpool(self.APC_CMD_NOMBATTV)))
            print("APC_CMD_VOUT: {}".format(self.smartpool(self.APC_CMD_VOUT)))
