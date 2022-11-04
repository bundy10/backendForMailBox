import RPi.GPIO as GPIO
import threading, time
import logging
from picamera import PiCamera
from time import sleep
from crypt import methods
import json
from tkinter import SW
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS


logging.basicConfig(level=logging.DEBUG)

camera = PiCamera()
def takePicture():
    
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/mailbox/Pictures/image.jpg')
    camera.stop_preview()


GPIO.setmode(GPIO.BCM)

solenoid = 2
Bled = 5
flashes = 3
doorswitch = 21
Yled = 10
button = 8
running = True
state = 1




class LED:
	
	channel = 0

	def __init__(self, channel):
		
		self.channel = channel

		GPIO.setup(self.channel, GPIO.OUT)

	def on(self):
		
		GPIO.output(self.channel, GPIO.HIGH)

		return "on"

	def off(self):

		GPIO.output(self.channel, GPIO.LOW)

		return "off"

class States:

	def state1():
		while(running):
			#state waiting for delivery
			while state == 1:
				if GPIO.input(button) == 0:
					GPIO.output(Yled, GPIO.HIGH)
					global state
					state = 2
					States.state2()

	def state2():
		#state waiting for user to unlock
		GPIO.output(Yled, GPIO.LOW)
		GPIO.output(Bled, GPIO.HIGH)
		GPIO.output(solenoid, GPIO.LOW)
		while state == 2:
			if GPIO.input(doorswitch) == 1:
				global state
				state = 3
				States.state3()
	
	def state3():
		#state while door is open 
		GPIO.output(Bled, GPIO.LOW)
		while state == 3:
			print("door open")
			if GPIO.input(doorswitch) == 0:
				global state
				state = 4
				States.state4()

	def state4():
			#state triggered by door closing
			#takes photo
			print("locked")
			GPIO.output(solenoid, GPIO.HIGH)
			GPIO.output(flashes, GPIO.HIGH)
			takePicture()
			time.sleep(3)
			GPIO.output(flashes, GPIO.LOW)
			global state
			state = 1
		



class Switch:

	def __init__(self, channel):
		
		self.channel = channel

		GPIO.setup(self.channel, GPIO.IN)

	def isTriggered(self):
		
		return GPIO.input(self.channel)




States.state1()