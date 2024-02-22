import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 26

GPIO.setup(PIR_PIN, GPIO.IN)

while True:
	if GPIO.input(PIR_PIN):
		print("On")
	else:
		print("Off")
	time.sleep(1)

