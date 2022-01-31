from adafruit_servokit import ServoKit
import sqlite3
import time
import RPi.GPIO as GPIO

#Setting the GPIO mode to BCM as opposed to BOARD. This is because the ServoKit library uses BCM so to use BOARD would result in a clash
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.OUT)

#Initiate PCA9685 servo controller
kit = ServoKit(channels = 16)
	
def tap():
	kit.servo[3].angle = 120 #Rotate the third servo to 120 degrees
	time.sleep(1)
	kit.servo[1].angle = 90
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	kit.servo[4].angle = 115
	time.sleep(1)
	kit.servo[0].angle = 60
	time.sleep(1)
	kit.servo[1].angle = 30
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	kit.servo[3].angle = 90
	time.sleep(1)
	kit.servo[1].angle = 40
	time.sleep(1)        
	GPIO.output(5, GPIO.HIGH) #Turn the tap on
	time.sleep(2.5)
	GPIO.output(5, GPIO.LOW) #Turn the tap off
		
def Americano():
	print("Americano")
	kit.servo[4].angle = 115
	time.sleep(1)
	kit.servo[1].angle = 0
	time.sleep(1)
	kit.servo[0].angle = 20
	time.sleep(1)
	kit.servo[3].angle = 140
	time.sleep(1)
	kit.servo[2].angle = 20
	time.sleep(1)
	kit.servo[4].angle = 150
	time.sleep(1)
	kit.servo[1].angle = 40
	time.sleep(1)
	kit.servo[3].angle = 90
	time.sleep(1)
	kit.servo[2].angle = 90
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	tap()
	
def Latte():
	print ("Latte")
	kit.servo[4].angle = 115
	time.sleep(1)
	kit.servo[0].angle = 70
	time.sleep(1)
	kit.servo[2].angle = 105
	time.sleep(1)
	kit.servo[3].angle = 150
	time.sleep(1)
	kit.servo[1].angle = 0
	time.sleep(1)
	kit.servo[4].angle = 150
	time.sleep(1)
	kit.servo[1].angle = 30
	time.sleep(1)
	kit.servo[2].angle = 90
	time.sleep(1)
	kit.servo[3].angle = 90
	time.sleep(1)
	kit.servo[1].angle = 40
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	tap()
	
def Cappuccino():
	print("Cappuccino")
	kit.servo[4].angle = 115
	time.sleep(1)
	kit.servo[2].angle = 50
	time.sleep(1)
	kit.servo[0].angle = 60
	time.sleep(1)
	kit.servo[1].angle = 10
	time.sleep(1)
	kit.servo[4].angle = 150
	time.sleep(1)
	kit.servo[2].angle = 100
	time.sleep(1)
	kit.servo[1].angle = 20
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	kit.servo[1].angle = 40
	time.sleep(1)
	kit.servo[2].angle = 90
	time.sleep(1)
	kit.servo[3].angle = 90
	time.sleep(1)
	tap()
	
def Tea():
	print ("Tea")
	kit.servo[4].angle = 115
	time.sleep(1)
	kit.servo[0].angle = 120
	time.sleep(1)
	kit.servo[2].angle = 70
	time.sleep(1)
	kit.servo[4].angle = 150
	time.sleep(1)
	kit.servo[2].angle = 90
	time.sleep(1)
	kit.servo[0].angle = 90
	time.sleep(1)
	tap()
	
while True:
	#Check if any of the pins have gone high, which would signal an order from the other Raspberry Pi
	if GPIO.input(6) == GPIO.HIGH:
		Americano()
	elif GPIO.input(13) == GPIO.HIGH:
		Cappuccino()
	elif GPIO.input(19) == GPIO.HIGH:
		Latte()
	elif GPIO.input(26) == GPIO.HIGH:
		Tea()

