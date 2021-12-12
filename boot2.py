# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import machine
import network
import time
#time.sleep(3)
lan = network.LAN(mdc = machine.Pin(23), mdio = machine.Pin(18), power= machine.Pin(16), phy_type = network.PHY_LAN8720, phy_addr=1)
lan.active(1)
lan.ifconfig()

#import webrepl
#webrepl.start('1234')

execfile('test.py')
