import RPi.GPIO as GPIO
import time
import requests

stop = False

beeping = False
busy = False

fpurl = "https://g7p6olvo4b.execute-api.ap-southeast-1.amazonaws.com/prod/foot-pedal"

def run():
	try:
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(17, GPIO.OUT)

		GPIO.output(17, GPIO.HIGH)

		
		def callback(channel):
			global beeping
			global busy

			print("Ok!", GPIO.input(27), beeping, busy)
			if GPIO.input(27) and not beeping:
				beeping = True
				
				GPIO.output(17, GPIO.LOW)
				time.sleep(0.25)
				GPIO.output(17, GPIO.HIGH)

				if not busy:
					busy = True
					print("POSTING")
					requests.post(fpurl, json={})
					busy = False
			else:
				beeping = False
				GPIO.output(17, GPIO.HIGH)
				
		GPIO.add_event_detect(27, GPIO.BOTH, callback=callback)

		
		while True:
			time.sleep(2)
			if GPIO.input(22):
				print("Motion")
				pass


	except KeyboardInterrupt:
		global stop
		stop = True
		GPIO.cleanup()
	except Exception as e:
		print("An error occurred:", e)

while not stop:
	run()
