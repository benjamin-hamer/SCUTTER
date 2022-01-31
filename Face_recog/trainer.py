import cv2
import os
import numpy as np
from PIL import Image
import sqlite3
import security

recognizer = cv2.createLBPHFaceRecognizer()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
cam = cv2.VideoCapture(0)

con = sqlite3.connect('Users.db')
cur = con.cursor()

s = security.Security

def create_db():
	with con:
		cur.execute("INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?);", (Id, name, 0, 0, 0, 0))
		con.commit()
		nameID = name+str(Id)
		cur.execute("INSERT INTO USERSPASS VALUES (?, ?, ?);", (nameID, passHash, Id))
		con.commit()

Id=raw_input('Enter your id: ')
name=raw_input('Enter your name: ')
passwordCreation = False
while passwordCreation == False:
	password=raw_input("Enter password: ")
	password2=raw_input("Confirm password: ")
	if password == password2:
		s = security.Security(password, 0)
		passHash=s.hashPassword()
		passwordCreation = True
	else:
		print ("Try again")
		
sampleNum=0
while True:
	ret, img = cam.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = detector.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		#Incrementing sample number by one
		sampleNum=sampleNum+1
		#Saving the captured face in the dataset folder
		cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
		#Show the image to be saved
		cv2.imshow('frame',img)
	#Wait for 100 ms
	if cv2.waitKey(100) & 0xFF == ord('q'):
		break
	#Break if the sample number is more than 30
	elif sampleNum>30:
		break
        
create_db()
cam.release()
cv2.destroyAllWindows()


def getImagesAndLabels(path):
    #Get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faceSamples=[]
    Ids=[]
    for imagePath in imagePaths:
        #Load the image and convert it into grayscale
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        #Getting the ID from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        #Extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids

#Delete the previous trainer.yml in order to replace it with the new one
os.system("sudo rm trainer/trainer.yml")
faces,Ids = getImagesAndLabels('dataSet')
recognizer.train(faces, np.array(Ids))
recognizer.save('trainer/trainer.yml')
