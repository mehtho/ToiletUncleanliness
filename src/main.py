import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import busio
import board
import boto3
from decimal import Decimal
import RPi.GPIO as GPIO
import math
import mpu6050 as mpu
import json

# Frequency
FREQ = 2

stop = False

def run():
	try:
		# Set up ADS1115
		i2c = busio.I2C(board.SCL, board.SDA)
		ads = ADS.ADS1115(i2c)
		channel = AnalogIn(ads, ADS.P0)

		# Set up MPU6050
		mpu6050 = mpu.mpu6050(0x68)

		# Set up AWS
		file = open('keys.txt', 'r')
		acki = file.readline().strip()
		asak = file.readline().strip()

		ddb = boto3.resource(
			"dynamodb",
			region_name="ap-southeast-1",
			aws_access_key_id=acki,
			aws_secret_access_key=asak
			)
		raw = ddb.Table("toilet-data")

		# Data Format
		class Record():
			def __init__(self, gyr, has_motion, pressure):
				self.timestamp = math.floor(time.time() * 1000)
				self.gyr = gyr
				self.has_motion = has_motion
				self.pressure = pressure

		# Set up PIR
		GPIO.setmode(GPIO.BCM)
		PIR_PIN = 23
		GPIO.setup(PIR_PIN, GPIO.IN)

		print('Startup, give it 3 seconds')
		time.sleep(3)
		print('READY')

		while True:
			rec = Record(
				mpu6050.get_accel_data(), 
				GPIO.input(PIR_PIN), 
				32767 - channel.value)
			
			if all(value == 0 for value in rec.gyr.values()):
				raise Exception
			
			item = json.loads(json.dumps(rec.__dict__), parse_float=Decimal)
			print(item)
			raw.put_item(Item=item)
			
			time.sleep(FREQ)

	except KeyboardInterrupt:
		global stop
		stop = True
		GPIO.cleanup()
	except Exception as e:
		print("An error occurred:", e)
	

while not stop:
	run()