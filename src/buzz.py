import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.HIGH)

def callback(channel):
	if GPIO.input(27):
		GPIO.output(17, GPIO.LOW)
		time.sleep(.25)
	else:
		GPIO.output(17, GPIO.HIGH)
		
GPIO.add_event_detect(27, GPIO.BOTH, callback=callback)

try:
	while True:
		time.sleep(.25)
except KeyboardInterrupt:
	GPIO.cleanup()
