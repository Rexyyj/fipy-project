# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
import pycom
import time
from machine import Timer
from pycoproc_2 import Pycoproc
from network import Bluetooth

from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12

class Sensor():

	def __init__(self):
		self.ble_ready = False
		self.wifi_ready = False
		self.chr1=None
		self.temp=0.0
		self.hum=0.0
		# check device
		py = Pycoproc()
		if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
			raise Exception('Not a Pysense')
		# check pybyte
		if 'pybytes' in globals():
			if(pybytes.isconnected()):
				self.wifi_ready=True
				print('Pybytes is connected, sending signals to Pybytes')
		# define devices
		self.bluetooth = Bluetooth()
		self.si = SI7006A20(py)
		self.li = LIS2HH12(py)


	def conn_cb(self,chr):
		events = chr.events()
		if events & Bluetooth.CLIENT_CONNECTED:
			print('client connected')
			self.ble_ready=True
		elif events & Bluetooth.CLIENT_DISCONNECTED:
			print('client disconnected')
			self.ble_ready = False

	def chr1_handler(self,chr, data):
		events = chr.events()
		print("events: ",events)
		if events & (Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT):
			val ="temp:"+str(round(self.temp, 2))+" hum:"+str(round(self.hum,2))
			chr.value(val)
		if (events & Bluetooth.CHAR_SUBSCRIBE_EVENT):
			self.ble_ready = True

	def bluetooth_enable(self):
		self.bluetooth.set_advertisement(name='fiPy_rex', manufacturer_data="Pycom", service_uuid=0xec00)

		self.bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.conn_cb)
		self.bluetooth.advertise(True)
		srv1 = self.bluetooth.service(uuid=0xec00, isprimary=True,nbr_chars=1)
		self.chr1 = srv1.characteristic(uuid=0xec0e, value='read_from_here') #client reads from here
		self.chr1.callback(trigger=(Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT), handler=self.chr1_handler)

	# generate different color for different pitch and roll
	def get_col(self,roll,pitch):
		if roll > 5 :
			r = 0xFF0000
		elif roll < -5:
			r = 0x0F0000
		else:
			r = 0x0000FF

		if pitch > 5:
			g = 0xFF00
		elif pitch<-5:
			g = 0x0F00
		else:
			g = 0x0000 
		return r+g


	# define handlers
	def data_update_handler(self,update_alarm):
		self.temp = self.si.temperature()
		self.hum = self.si.humidity()

	def wifi_handler(self,update_alarm):
		print("wifi handler running")
		if self.wifi_ready:
			pybytes.send_signal(2,self.temp)
			pybytes.send_signal(3,self.hum)
    

	def ble_handler(self,update_alarm):
		print("ble handler running")
		if self.ble_ready:
			self.chr1.value("temp:"+str(round(self.temp, 2))+" hum:"+str(round(self.hum,2)))

	def led_handler(self,update_alarm):
		col = self.get_col(self.li.roll(),self.li.pitch())
		pycom.rgbled(col)

	def main(self):
		self.bluetooth_enable()
		alarms = []
		alarms.append(Timer.Alarm(self.data_update_handler,s=1, periodic=True))
		alarms.append(Timer.Alarm(self.led_handler,ms=500, periodic=True))
		alarms.append(Timer.Alarm(self.ble_handler,s=5, periodic=True))
		alarms.append(Timer.Alarm(self.wifi_handler,s=10, periodic=True))
		while True:
			i = input("Press q to exit")
			if i == "q":
				for alarm in alarms:
					alarm.cancel()
				break
			else:
				pass


if __name__=="__main__":
	pycom.heartbeat(False)
	sensor=Sensor()
	sensor.main()



