import cv2
import numpy as np
import sqlite3
from Tkinter import *
import os
import RPi.GPIO as GPIO
from time import sleep # Load the required modules/libraries


#set up the face detection system
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath);

#initiate the GPIO pins for communication with the other Raspberry Pi
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

#Initialise the camera for facial recognition
cam = cv2.VideoCapture(0)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)

#Connect to the database
con = sqlite3.connect('Users.db')
cur = con.cursor()

#Define the pin numbers
americanoPin = 31
cappuccinoPin = 33
lattePin = 35
teaPin = 37

class Face_ID:
	def __init__(self, Id):
		self.Id = str(Id)
		
	def americano(self):
		#Send the signal to make an Americano
		GPIO.output(americanoPin, GPIO.HIGH)
		sleep(1)
		GPIO.output(americanoPin, GPIO.LOW)
		#Update the database by incrementing the value of Americano by one
		cur.execute("UPDATE USERS SET AMERICANO=AMERICANO+1 WHERE ID=?;", (self.Id))
		print ("Database updated")
		con.commit()

	def cappuccino(self):
		GPIO.output(cappuccinoPin, GPIO.HIGH)
		sleep(1)
		GPIO.output(cappuccinoPin, GPIO.LOW)
		cur.execute("UPDATE USERS SET CAPPUCCINO=CAPPUCCINO+1 WHERE ID=?;", (self.Id))
		con.commit()

	def latte(self):
		GPIO.output(lattePin, GPIO.HIGH)
		sleep(1)
		GPIO.output(lattePin, GPIO.LOW)
		cur.execute("UPDATE USERS SET LATTE=LATTE+1 WHERE ID=?;", (self.Id))
		con.commit()


	def tea(self):
		GPIO.output(teaPin, GPIO.HIGH)
		sleep(1)
		GPIO.output(teaPin, GPIO.LOW)
		cur.execute("UPDATE USERS SET TEA=TEA+1 WHERE ID=?;", (self.Id))
		con.commit()	
	
	def autoSelect(self):
		#Get the values of all the drinks in the database
		cur.execute("SELECT CAPPUCCINO FROM USERS WHERE ID=?;", (self.Id))
		cappuccinoValue = cur.fetchall()
		cur.execute("SELECT AMERICANO FROM USERS WHERE ID=?;", (self.Id))
		americanoValue = cur.fetchall()
		cur.execute("SELECT LATTE FROM USERS WHERE ID=?;", (self.Id))
		latteValue = cur.fetchall()
		cur.execute("SELECT TEA FROM USERS WHERE ID=?;", (self.Id))
		teaValue = cur.fetchall()
		#Find the highest value
		favourite = max(cappuccinoValue, americanoValue, latteValue, teaValue)
		if favourite == cappuccinoValue:
			selection = cappuccinoPin
		elif favourite == americanoValue:
			selection = americanoPin
		elif favourite == latteValue:
			selection = lattePin
		elif favourite == teaValue:
			selection = teaPin
		print ("Choice made successfully")
		#Order the favourite drink
		GPIO.output(selection, GPIO.HIGH)
		sleep(1)
		GPIO.output(selection, GPIO.LOW)

	def options(self):
		rootWindow = Tk()
		rootWindow.title("Menu")
		rootWindow.geometry("160x360")
		label1 = Label(rootWindow,text = "Select your choice:")
		label1.grid()
		button1 = Button(rootWindow,text = "Americano",command = Face_ID(self.Id).americano)
		button1.grid()
		button2 = Button(rootWindow,text = "Cappucino",command = Face_ID(self.Id).cappuccino)
		button2.grid()
		button3 = Button(rootWindow,text = "Latte",command = Face_ID(self.Id).latte)
		button3.grid()
		button5 = Button(rootWindow,text = "Tea",command = Face_ID(self.Id).tea)
		button5.grid()
		rootWindow.mainloop()
		rootWindow.after(50000, Face_ID(self.Id).autoSelect()) #After 50000 ms (50 seconds) run the autoselect function
		
	def faceID(self):
		complete = False
		while complete == False:
			ret, im = cam.read()
			cv2.imshow('im',im) 
			gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			faces = faceCascade.detectMultiScale(gray, 1.2,5)
			for(x,y,w,h) in faces:
				cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)# Draw a rectangle round the face
				self.Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
				self.Id = str(self.Id)
				if(conf<50): # If more than 50% match 
					cur.execute("SELECT NAME FROM USERS WHERE ID = ?;", (self.Id))# Retrieve name from database
					nameid = cur.fetchall()
				else:
					nameid = 'Unknown'
					cv2.cv.PutText(cv2.cv.fromarray(im),str(nameid), (x,y+h),font, 255) #Wite unknown in the box round the face
				if nameid != 'Unknown':
					complete = True
					cam.release()
					cv2.destroyAllWindows()
					Face_ID(self.Id).options()
			if cv2.waitKey(10) & 0xFF==ord('q'):
				break
		cam.release()
		cv2.destroyAllWindows()

f = Face_ID(0)
f.faceID()
