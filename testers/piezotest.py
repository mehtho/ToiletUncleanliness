import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 17

GPIO.setup(PIR_PIN, GPIO.IN)

print('Startup')
time.sleep(1)
print('READY')

while True:
	if not GPIO.input(PIR_PIN):
		print("Sitting")
	time.sleep(1)

