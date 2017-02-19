# coding: utf-8

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import threading

from neopixel import *

# LED strip configuration:
#LED_COUNT      = 10      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class Myneopixel():
	
	
	# Define functions which animate LEDs in various ways.
	def colorWipe(self, strip, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
			strip.show()
			mysleep(wait_ms)
			if self.stop_event.is_set(): break
	
	def theaterChase(self, strip, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, color)
				strip.show()
				mysleep(wait_ms)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)
				if self.stop_event.is_set(): break
			if self.stop_event.is_set(): break
	
	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)
	
	def rainbow(self, strip, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, wheel((i+j) & 255))
			strip.show()
			mysleep(wait_ms)
			if self.stop_event.is_set(): break
	
	def rainbowCycle(self, strip, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256*iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			strip.show()
			mysleep(wait_ms)
			if self.stop_event.is_set(): break

	def theaterChaseRainbow(self, strip, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, wheel((i+j) % 255))
				strip.show()
				mysleep(wait_ms)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)
				if self.stop_event.is_set(): break
			if self.stop_event.is_set(): break

	def target(self):
		while not self.stop_event.is_set():
			# Color wipe animations.
			if not self.stop_event.is_set(): self.colorWipe(strip, Color(255, 0, 0))
			if not self.stop_event.is_set(): self.colorWipe(strip, Color( 0,255, 0))
			if not self.stop_event.is_set(): self.colorWipe(strip, Color(0, 0, 255))
				
			# Theater chase animations.
			if not self.stop_event.is_set(): self.theaterChase(strip, Color(127, 127, 127))  # White theater chase
			if not self.stop_event.is_set(): self.theaterChase(strip, Color(127,   0,   0))  # Red theater chase
			if not self.stop_event.is_set(): self.theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
			# Rainbow animations.
			if not self.stop_event.is_set(): self.rainbow(strip)
			if not self.stop_event.is_set(): self.rainbowCycle(strip)
			if not self.stop_event.is_set(): self.theaterChaseRainbow(strip)


	# for abort thread process
	def mysleep(self, wait_ms):
		# check thread abord or not
		if not self.stop_event.is_set():
			time.sleep(wait_ms/1000.0)
	
	def clearLED(self):
		"""すべて消灯させる"""
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0, 0, 0))
			strip.show()
		
	def startDemo(self):
		self.stop_event = threading.Event() #停止させるかのフラグ

		"""デモをスレッド動作させる"""
		self.thread = threading.Thread(target = self.target)
		self.thread.start()
	
	def stopDemo(self):
		"""スレッドを停止させる"""
		if not self.stop_event.is_set():
			self.stop_event.set()
			self.thread.join()    #スレッドが停止するのを待つ
			self.clearLED()		

	def __init__(self, count, pin):
		# define strip object.
		#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		strip = Adafruit_NeoPixel(count, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		# Intialize the library (must be called once before other functions).
		strip.begin()
