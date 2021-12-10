#from machine import UART;
import apcsmartups
import time;

ups = apcsmartups.ApcSmartUps(tx=32, rx=33)
if ups.UPSlinkCheck():
    print(ups.smartpool(ups.APC_CMD_IDEN))
#    s = ups.smartpool(ups.APC_CMD_UPSMODEL)
#    print(s)

#uart1 = UART(1, baudrate=2400, bits=8, parity=None, stop=1, tx=32, rx=33)
import time
#, bits=8, parity=None, stop=1
#uart1 = UART(2, baudrate=2400, bits=8, parity=None, stop=1, tx=32, rx=33)
#uart1.write('Y')  # write 5 bytes
#r = uart1.readline()         # read up to 5 bytes
#print(r)
# uart1.write('Y');time.sleep(0.2);print(uart1.readline())



# mpremote connect port:/dev/ttyUSB0 mount .
# Local directory . is mounted at /remote
# Connected to MicroPython at /dev/ttyUSB0
# Use Ctrl-] to exit this shell
# >
# MicroPython v1.17-220-gb491967bb on 2021-12-06; ESP32-ETH01 with ESP32
# Type "help()" for more information.
# >>> from machine import UART;import time;uart1 = UART(1, baudrate=2400, bits=8, parity=None, stop=1, tx=32, rx=33)
# >>> uart1.write('Y');time.sleep(0.2);print(uart1.readline())
# 1
# b'Y'
# >>> uart1.write('Y');time.sleep(0.2);print(uart1.readline())
# 1
# b'SM\r\n'
# >>>
