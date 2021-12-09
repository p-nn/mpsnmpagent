import time
from machine import UART


class ApcSmartUps:
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

    APC_CMD_UPSMODEL = b''+chr(0x01) #bytes.fromhex('01')  # Model number
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
    APC_CMD_SENS = b's'  # Sensitivity
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
    APC_CMD_BATTDAT = b'x'  # serial number
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
    APC_CMD_EPROM = b''+chr(0x1a) #bytes.fromhex('1a')  # Valid eprom values
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

    DISCHARGE = 'D'
    CHARGE_LIM = 25

    UPS_ENABLED = '?'
    UPS_ON_BATT = '!'
    UPS_ON_LINE = '$'
    UPS_REPLACE_BATTERY = '#'
    BATT_LOW = '%'
    BATT_OK = '+'
    UPS_EPROM_CHANGE = '|'
    UPS_TRAILOR = ':'
    UPS_LF = '\n'
    UPS_CR = '\r'

    SUCCESS = 0  # Function successfull */
    FAILURE = 1  # Function failure */

#    def __init__(self, port='/dev/ttyS)'):
    def __init__(self):
        self.online = False
        self.stat = ''
        try:
#            self.serialport = serial.Serial(port=port, baudrate=2400, parity=serial.PARITY_NONE, stopbits=1, xonxoff=0,
#                                            bytesize=8)
            self.serialport = UART(1, baudrate=2400, bits=8, parity=None, stop=1, tx=32, rx=33)
            self.UPSlinkCheck()
            # self.stat = self.smartpool(APC_CMD_UPS_CAPS)
        except:
            pass

    def UPSlinkCheck(self):
        self.online = False
        self.serialport.write(b'Y')  # write a string
        r = self.serialport.readline()
        if r == b'SM\r\n':
            self.online = True
        return self.online

    def close(self):
        #self.serialport.close()
        pass

    def smartpool(self, cmd):  # read data without \r\n
        self.serialport.write(cmd)
        print(cmd)
        time.sleep(1)
        stat = self.serialport.readline()
        print(stat)
        return stat[:-2]  # drop final \r\n

    def change_ups_eeprom_item(self, cmd, bytes):
        #self.serialport.timeout = 4
        #self.serialport.timeout = 4

        self.serialport.write(cmd)
        oldname = self.serialport.readline()

        print('set new name:  {}'.format(bytes))
        print("old name     : {}".format(oldname))

        #self.serialport.write_timeout = 4
        self.serialport.write(self.APC_CMD_CYCLE_EPROM)
        time.sleep(1)
        arr = bytearray(bytes)
        for i in range(len(bytes)):
            self.serialport.write(arr[i:i + 1])
            print('write to ups {}'.format(arr[i:i + 1]))
            time.sleep(1)
        response = self.serialport.readline()
        print("Response: {}".format(response))
        if response != b'OK\r\n':
            print("\nError changing UPS name\n")
        #self.serialport.write_timeout = 1
        #self.serialport.timeout = 1
        self.serialport.write(cmd)

        return self.serialport.readline()

    def change_ups_name2(self, newname):
        newname = newname.encode().ljust(8, b' ')
        return self.change_ups_eeprom_item(self.APC_CMD_IDEN, newname)

    def change_ups_battery_date(self, newdate):
        # print(newdate)
        # month = int(newdate[0:2])
        # day = int(newdate[3:5])
        # year = int(newdate[6:8])
        # res = month>0 & month<13 & day > 0 & day<32
        # print(str(newdate[0:2]),str(newdate[3:5]),str(newdate[6:8]),month,day,year,res)
        newdate = newdate.encode().ljust(8, b' ')
        #            res = True
        return self.change_ups_eeprom_item(self.APC_CMD_BATTDAT, newdate)

    def change_ups_name(self, newname):
        #self.serialport.timeout = 4
        newname = newname.encode().ljust(8, b' ')

        self.serialport.write(self.APC_CMD_IDEN)
        oldname = self.serialport.readline()

        print('set new name: {}'.format(newname))
        print("APC_CMD_IDEN: {}".format(oldname))

        #self.serialport.write_timeout = 4
        self.serialport.write(self.APC_CMD_CYCLE_EPROM)
        time.sleep(1)
        arr = bytearray(newname)
        for i in range(8):
            self.serialport.write(arr[i:i + 1])
            print('write to ups {}'.format(arr[i:i + 1]))
            time.sleep(1)
        response = self.serialport.readline()
        print("Response: {}".format(response))
        if response != 'OK':
            print("\nError changing UPS name\n")
        #self.serialport.write_timeout = 1
        #self.serialport.timeout = 1
        self.serialport.write(self.APC_CMD_IDEN)

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

