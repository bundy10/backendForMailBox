from crypt import methods
import json
from tkinter import SW
from flask import Flask
from flask import request
import RPi.GPIO as GPIO
import Controll
from Controll import LED, Switch, States


solenoid = 2
Bled = 5
flashes = 3
doorswitch = 21
Yled = 10
button = 8

GPIO.setup(solenoid, GPIO.OUT)
GPIO.setup(Bled, GPIO.OUT)
GPIO.setup(flashes, GPIO.OUT)
GPIO.setup(Yled, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(doorswitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#Pre-Cleanup (Some I/O states stick around far longer than they should)
GPIO.output(Yled, GPIO.LOW)
GPIO.output(Bled, GPIO.LOW)
GPIO.output(solenoid, GPIO.HIGH)
GPIO.output(flashes, GPIO.LOW)


States.state1()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
	
	action = request.values['action']

	led = LED(17)

	if action == 'on':
		led.on()

	if action == 'off':
		led.off()

	if action == 'accept':
		States.state2

	return 'success'

@app.route('/switch', methods=['GET'])
def button():

	button = Switch(25)

	response = app.response_class(
        response={"switchStatus" : str(button.isTriggered())},
        status=200,
        mimetype='application/json'
	)
	return response
