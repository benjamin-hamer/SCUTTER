import sqlite3
import hashlib 

con = sqlite3.connect('UsersPasswords.db')
cur = con.cursor()

class Security:
	def __init__ (self, password, username):
		self.password = password
		self.username = username
		
	def setPassword(self):
		password = self.password
		result = hashlib.md5(password.encode()) 
		return result.hexdigest()

	def createUser(self):
		cur.execute("INSERT INTO USERS VALUES (?, ?);", (self.username, s.setPassword()))
		con.commit()

username = input("Please enter your username")
password = input("Please enter your password")
s = Security(password, username)
s.createUser()
