# coding: utf-8

import myneopixel
import time

#import wiringpi

# initialize GPIO
#io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
#io.pinMode(24, io.INPUT)

import RPi.GPIO as GPIO

portStatus = GPIO.LOW

def myCallBack(channel):
	global portStatus
  
	if channel == 24:
		if portStatus == GPIO.LOW:
			portStatus = GPIO.HIGH
			#print("HIGH")
			myneopixel.startDemo()
		else:
			portStatus = GPIO.LOW
			#print("LOW")
			myneopixel.stopDemo()

# Main program logic follows:
if __name__ == '__main__':

	# Create NeoPixel object with appropriate configuration.
	#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	#strip.begin()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(24, GPIO.RISING, callback=myCallBack, bouncetime=200)
 
	try:
		while True:
			time.sleep(0.01)
	except KeyboardInterrupt:
		myneopixel.stopDemo()
		GPIO.cleanup()
