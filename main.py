import time
import busio
import board
import boto3
from decimal import Decimal
import adafruit_amg88xx
import RPi.GPIO as GPIO
import math
import mpu6050
import json

# Frequency
FREQ = 2

# Set up thermal AMG8833
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

mpu6050 = mpu6050.mpu6050(0x68)

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
raw = ddb.Table("raw-data")

def read_acc_temp():
    gyroscope_data = mpu6050.get_gyro_data()
    temperature = mpu6050.get_temp()

    return gyroscope_data, temperature

class Record():
    def __init__(self, therm, gyr, ambient_temp, has_motion, has_puddle=False):
        self.timestamp = math.floor(time.time() * 1000)
        self.therm = therm
        self.gyr = gyr
        self.ambient_temp = ambient_temp
        self.has_motion = has_motion
        self.has_puddle = has_puddle

# Set up PIR
GPIO.setmode(GPIO.BCM)
LABEL_PIN = 26
PIR_PIN = 27

GPIO.setup(LABEL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIR_PIN, GPIO.IN)

print('Startup, give it 3 seconds')
time.sleep(3)
print('READY')

while True:
    gyroscope, ambient = read_acc_temp()
    rec = Record(amg.pixels, gyroscope, ambient, GPIO.input(PIR_PIN), GPIO.input(LABEL_PIN))
    
    item = json.loads(json.dumps(rec.__dict__), parse_float=Decimal)
    print(item)
    raw.put_item(Item=item)
    
    time.sleep(FREQ)
