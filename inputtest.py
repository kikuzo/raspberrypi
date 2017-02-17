# coding: utf-8
import RPi.GPIO as GPIO
import time
 
portStatus = GPIO.LOW
 
def myCallBack(channel):
 global portStatus
  
 if channel == 24:
  if portStatus == GPIO.LOW:
   portStatus = GPIO.HIGH
   print("HIGH")
   #GPIO.output(25, GPIO.LOW)
  else:
   portStatus = GPIO.LOW
   print("LOW")
   #GPIO.output(25, GPIO.HIGH)
 
GPIO.setmode(GPIO.BCM)
#GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=myCallBack, bouncetime=200)
 
try:
 while True:
  time.sleep(0.01)
except KeyboardInterrupt:
 GPIO.cleanup()
 