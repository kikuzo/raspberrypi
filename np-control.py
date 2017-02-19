# coding: utf-8

import myneopixel
import time

#import wiringpi

# initialize GPIO
#io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
#io.pinMode(24, io.INPUT)

import RPi.GPIO as GPIO

LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)

TOGGLE_BUTTON_PIN = 24
portStatus = GPIO.LOW

def myCallBack(channel):
	global portStatus
  
	if channel == TOGGLE_BUTTON_PIN:
		if portStatus == GPIO.LOW:
			portStatus = GPIO.HIGH
			mynp.startDemo()
		else:
			portStatus = GPIO.LOW
			mynp.stopDemo()

# Main program logic follows:
if __name__ == '__main__':

	''' neoPixelを操作するクラスを生成'''
	mynp = myneopixel.Myneopixel(LED_COUNT, LED_PIN)	

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TOGGLE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(TOGGLE_BUTTON_PIN, GPIO.RISING, callback=myCallBack, bouncetime=200)
 
	try:
		while True:
			time.sleep(0.01)
	except KeyboardInterrupt:
		mynp.stopDemo()
		GPIO.cleanup()
