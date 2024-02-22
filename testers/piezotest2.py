import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)

def read_sensor_data():
   return channel.value, channel.voltage

# Start a while loop to continuously read the sensor data
while True:
    print(read_sensor_data())

    # Wait for 1 second
    time.sleep(1)
