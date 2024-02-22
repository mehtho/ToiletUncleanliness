import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 23

GPIO.setup(PIR_PIN, GPIO.IN)

print('Startup')
time.sleep(1)
print('READY')

while True:
	if GPIO.input(PIR_PIN):
		print("Motion Detected")
	time.sleep(1)

