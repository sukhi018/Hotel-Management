import re
import sqlite3 as sql
import os
# import random


#-------------------- REGEX ------------------------#

username_re = re.compile('\\w{4,8}')
password_re = re.compile('[A-z0-9@?#$%^&*]{8,16}')
fullname_re = re.compile('([A-z]{2,26}\\s[A-z]{1,20}|[A-z]{2,20})')
phn_no_re = re.compile('(9|8|7|6)\\d{9}')
email_re = re.compile('\\w+@(gmail|outlook|hotmail).(com|in|org)')
aadhaar_re = re.compile('\\d{4}\\s\\d{4}\\s\\d{4}')
date_re = re.compile('([2][0][2-9]\\d|[2][1-9]\\d{2}|[3-9]\\d{3})-([0][1-9]|[1][1-2])-([0][1-9]|[1-2]\\d|[3][0-1])')
time_re = re.compile('([0][1-9]|[1-2][012]):([0]\\d|[1-6]\\d)[AP][M]')


#------------------------------ DATABASE ---------------------------------------#

conn=sql.connect('hotel.db')
cur=conn.cursor()

#----------------------- CREATE TABLE QUERIES --------------------------#

create_ROOMS ="""
		CREATE TABLE IF NOT EXISTS ROOMS(
		ROOM_NO INT UNIQUE NOT NULL,
		STATUS INT(1) NOT NULL,
		PRICE_IN_RS INT NOT NULL,
		NAME VARCHAR,
		ADDRESS VARCHAR,
		PHN_NO INT,
		EMAIL VARCHAR,
		AADHAAR INT,
		DATE_OF_ARRIVAL DATE,
		DATE_OF_DEPARTURE DATE,
		TIME_OF_ARRIVAL TIME,
		TIME_OF_DEPARTURE TIME
		);
		"""

create_admin =  """
				CREATE TABLE IF NOT EXISTS ADMIN(
				USERNAME VARCHAR UNIQUE,
				PASSWORD VARCHAR,
				KEY INT(4)
				);
				"""

create_guest = """
		CREATE TABLE IF NOT EXISTS GUEST(
		USERNAME VARCHAR UNIQUE,
		PASSWORD VARCHAR
		);
		"""

#--------------- INSERT INTO TABLE QUERIES ---------------#

insert_query = """
	 	INSERT INTO ROOMS(ROOM_NO,STATUS,PRICE_IN_RS)
	 	VALUES (?,?,?);
	 """


insert_admin = """
			   INSERT INTO ADMIN(USERNAME, PASSWORD, KEY) VALUES(?,?,?);
			   """

insert_guest = """
			   INSERT INTO GUEST(USERNAME, PASSWORD) VALUES(?,?)
			   """

update_room = """
			  UPDATE ROOMS
			  SET STATUS=?, NAME=?, ADDRESS=?, PHN_NO=?, EMAIL=?,AADHAAR=?, DATE_OF_ARRIVAL=?,
			  DATE_OF_DEPARTURE=?,TIME_OF_ARRIVAL=?,TIME_OF_DEPARTURE=?
			  WHERE ROOM_NO = ?;
			  """

update_admin = """
			   UPDATE ADMIN
			   SET USERNAME=?, PASSWORD=?
			   WHERE KEY = ?;
			   """

update_key = """
			 UPDATE ADMIN
			 SET KEY = ?;
			 """

#-------------------- SHOW QUERIES ---------------------#

show_admin = """
			 SELECT * FROM ADMIN;
			 """

show = 	"""
		SELECT * FROM ROOMS WHERE STATUS = 0;
		"""

show_rooms = """
		SELECT ROOM_NO FROM ROOMS WHERE STATUS = 0;
		"""

check_price = 	"""
				SELECT ROOM_NO FROM ROOMS WHERE STATUS = 0 AND PRICE_IN_RS = (?);
				"""

show_guest = """
			 SELECT NAME, PHN_NO, ROOM_NO, DATE_OF_ARRIVAL, TIME_OF_ARRIVAL FROM ROOMS
			 WHERE NAME = ?;
			 """

show_guest_id = """
				SELECT * FROM GUEST WHERE USERNAME = ? AND PASSWORD = ?;
				"""

cur.execute(create_ROOMS)
cur.execute(create_admin)
cur.execute(create_guest)


prices=[]
for i in range(1,19):
	if i in range(1,7):
		prices.append((1000,))
	elif i in range(7,13):
		prices.append((1500,))
	else:
		prices.append((2000,))

try:
	cur.executemany(insert_query,[(i,0,prices[i-1][0]) for i in range(1,19)])
except Exception:
	pass

try:
	id_pswrd=list(cur.execute(show_admin))
	conn.commit()
	if id_pswrd==[]:
		cur.execute(insert_admin,('abhishek','abhi@123',2001))
except Exception:
	pass

conn.commit()


ck=list(cur.execute(show_rooms))
total=len(ck)
conn.commit()

clear = lambda: os.system('cls')

# id_pswrd=list(cur.execute(show_admin))
# conn.commit()
# print(id_pswrd[0][1])
#------------------------ CLASSES ------------------------#

class hotel:

	def enter():
		
		clear()
		x = input('\n1. ADMIN \n2. GUEST \n3. EXIT\n\n')
		if re.fullmatch('[1-3]',x):
			if int(x)==1:
				hotel.admin()
			elif int(x)==2:
				hotel.guest()
			elif int(x)==3:
				print('HAVE A NICE DAY'.center(40,'.'))
				exit()
		else:
			print('INVALID INPUT...\n')
			hotel.enter()

	def admin():
		
		clear()
		y = input('\n1. LOGIN\n2. SIGNUP\n3. GO BACK\n')
		if re.fullmatch('[1-3]',y):
			if int(y)==1:
				hotel.admin_login()
			elif int(y)==2:
				hotel.admin_signup()
			elif int(y)==3:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			hotel.admin()

	def admin_login():
		
		clear()
		id_pswrd=list(cur.execute(show_admin))
		conn.commit()
		x=input('\nPRESS 1 ENTER USERNAME AND PASSWORD OR 2 GO BACK\n')
		if re.fullmatch('[1-2]',x):
			if int(x)==1:
				u=input('USERNAME = ')
				p=input('PASSWORD = ')
				if u != id_pswrd[0][0] and p != id_pswrd[0][1]:
					print('\n\t\t-----INVALID USERNAME AND PASSWORD-----\n')
					hotel.admin_login()
				elif u == id_pswrd[0][0] and p != id_pswrd[0][1]:
					print('\n\t\t-----INVALID PASSWORD-----\n')
					hotel.admin_login()
				elif u == id_pswrd[0][0] and p == id_pswrd[0][1]:
					hotel.admin_fun()
				else:
					hotel.admin_login()
			elif int(x)==2:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			hotel.admin_login()
				

	def admin_signup():
		
		clear()
		x=input('\nPRESS 1 TO ENTER ADMIN KEY OR 2 TO GO BACK...\n\n')
		if re.fullmatch('[1-2]',x):
			if int(x)==1:
				hotel.admin_key()
			elif int(x)==2:
				hotel.admin()
		else:
			print('\nINVALID INPUT...\n')
			hotel.admin_signup()

	def admin_key():
		
		clear()
		k = input('ADMIN KEY(XXXX) = ')
		if re.fullmatch('\\d{4}',k):
			id_pswrd=list(cur.execute(show_admin))
			conn.commit()
			if int(k) == id_pswrd[0][2]:
				hotel.admin_userpwd()
			else:
				hotel.admin_key()
		else:
			print('\nINVALID ADMIN KEY...')
			hotel.admin_signup()

	def admin_userpwd():
		
		clear()
		id_pswrd=list(cur.execute(show_admin))
		conn.commit()
		x=input('\nPRESS 1 TO SET USERNAME AND PASSWORD & PRESS 2 TO GO BACK...\n')
		if re.fullmatch('[1-2]',x):
			if int(x)==1:
				u=input('USERNAME = ')
				if username_re.fullmatch(u)==None:
					print('\n\t\t INVALID USERNAME ONLY CONTAINS CHAR. OF RANGE(4,8) INCLUDED...')
					hotel.admin_userpwd()
				else:
					p=input('PASSWORD = ')
					if password_re.fullmatch(p)==None:
						print('\n\t\t INVALID PASSWORD CONTAIN ATLEAST 8 DIGITS...')
						hotel.admin_userpwd()
					else:
						cur.execute(update_admin,(u,p,id_pswrd[0][2]))
						hotel.admin()
			elif int(x)==2:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			admin_userpwd()

	def admin_fun():

		clear()
		y=input('\n1. CHANGE KEY\n2. AVAILABLE ROOMS\n3. CHECK GUESTS\n4. GO BACK\n')
		if re.fullmatch('[1-4]',y):
			if int(y)==1:
				hotel.change_key()
			elif int(y)==2:
				hotel.check_rooms()
			elif int(y)==3:
				hotel.check_guest()
			elif int(y)==4:
				hotel.admin()
		else:
			print('\nINVALID INPUT...\n')
			hotel.admin_fun()

	def change_key():
		
		clear()
		y=input('\nPRESS 1 TO ENTER NEW KEY OR 2 TO GO BACK...\n')
		if re.fullmatch('[1-2]',y):
			if int(y)==1:
				x=input('\nENTER NEW KEY(XXXX) = ')
				if re.fullmatch('\\d{4}',x) == None:
					print('\nINVALID KEY TYPE MUST BE INTEGER VALUES...')
					hotel.change_key()
				else:
					cur.execute(update_key,(x,))
					conn.commit()
					print('KEY UPDATED')
					hotel.admin_fun()

			elif int(y)==2:
				hotel.admin_fun()

		else:
			print('INVALID INPUT')
			hotel.change_key()


	def check_rooms():
		
		clear()
		SHOW=list(cur.execute(show))
		conn.commit()
		if ck==[]:
			print("-> ROOMS NOT AVAILABLE\n")
		else:
			print("ROOMS AVAILABLE -->",total,'\n\n')
			print('ROOM NO',"|",'  STATUS  ','   |','PRICES')
			print()
			for rows in SHOW:
				print((str(rows[0])).ljust(7),"|  ",'AVAILABLE','  |',"Rs",rows[2])
			x=input("\nPRESS B TO GO BACK\n")
			if x == ('b' or 'B'):
				hotel.admin_fun()
			else:
				hotel.check_rooms()

	def check_rooms_guest():
		
		clear()
		SHOW=list(cur.execute(show))
		conn.commit()
		if ck==[]:
			print("-> ROOMS NOT AVAILABLE\n")
		else:
			print("ROOMS AVAILABLE -->",total,'\n\n')
			print('ROOM NO',"|",'  STATUS  ','   |','PRICES')
			print()
			for rows in SHOW:
				print((str(rows[0])).ljust(7),"|  ",'AVAILABLE','  |',"Rs",rows[2])
			x=input("\nPRESS B TO GO BACK\n")
			if x == ('b' or 'B'):
				hotel.guest_fun()
			else:
				hotel.check_rooms_guest()

	def check_guest():
		
		clear()
		inp = input('\nPLEASE ENTER NAME OF GUEST\n')
		if list(cur.execute(show_guest,(inp,)))!=[]:
			details=list(cur.execute(show_guest,(inp,)))
			print('NAME         ->',details[0][0])
			print('PHONE NO.    ->',details[0][1])
			print('ROOM NO.     ->',details[0][2])
			print('ARRIVAL DATE ->',details[0][3])
			print('ARRIVAL TIME ->',details[0][4])
			x=input("\nPRESS B TO GO BACK\n")
			if x == ('b' or 'B'):
				hotel.admin_fun()
			else:
				hotel.admin_fun()

		else:
			print('\nSORRY, THE HOTEL HAS NO RESERVATION UNDER THAT NAME...')
			x=input("\nPRESS B TO GO BACK\n")
			if x == ('b' or 'B'):
				hotel.admin_fun()
			else:
				hotel.admin_fun()

	def price_service():
		
		clear()
		print('SELECT ROOMS PRICE AND SERVICES...\n')
		inp = input('1. Rs1000 (FOR 1 PERSON)\n2. Rs1500 (FOR 2 PERSON)\n3. Rs2000 (FOR 3 PERSON)\n4. GO BACK\n')
		if re.fullmatch('[1-4]',inp):
			if int(inp)==1:
				entry(1000)
			elif int(inp)==2:
				entry(1500)
			elif int(inp)==3:
				entry(2000)
			elif int(inp)==4:
				hotel.guest_fun()
		else:
			print('\nINVALID INPUT...\n')
			hotel.price_service()

	def guest():

		clear()
		y = input('\n1. LOGIN\n2. SIGNUP\n3. GO BACK\n')
		if re.fullmatch('[1-3]',y):
			if int(y)==1:
				hotel.guest_login()
			elif int(y)==2:
				hotel.guest_signup()
			elif int(y)==3:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			hotel.guest()

	def guest_login():

		clear()
		x=input('\nPRESS 1 ENTER USERNAME AND PASSWORD OR 2 GO BACK\n')
		if re.fullmatch('[1-2]',x):
			if int(x)==1:
				u=input('USERNAME = ')
				p=input('PASSWORD = ')
				if list(cur.execute(show_guest_id,(u,p)))==[]:
					print('\n\t\t-----INVALID USERNAME AND PASSWORD-----\n')
					hotel.guest_login()
				else:
					hotel.guest_fun()
			elif int(x)==2:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			hotel.admin_login()

	def guest_signup():

		clear()
		x=input('\nPRESS 1 TO SET USERNAME AND PASSWORD & PRESS 2 TO GO BACK...\n')
		if re.fullmatch('[1-2]',x):
			if int(x)==1:
				u=input('USERNAME = ')
				if username_re.fullmatch(u)==None:
					print('\n\t\t INVALID USERNAME ONLY CONTAINS CHAR. OF RANGE(4,8) INCLUDED...')
					hotel.guest_signup()
				else:
					p=input('PASSWORD = ')
					if password_re.fullmatch(p)==None:
						print('\n\t\t INVALID PASSWORD CONTAIN ATLEAST 8 DIGITS...')
						hotel.guest_signup()
					else:
						cur.execute(insert_guest,(u,p))
						hotel.guest()
			elif int(x)==2:
				hotel.guest()
		else:
			print('\nINVALID INPUT...\n')
			hotel.guest_signup()

	def guest_fun():

		clear()
		x=input('\n1. ROOMS \n2. BUY ROOM \n3. GO BACK\n')
		if re.fullmatch('[1-3]',x):
			if int(x)==1:
				hotel.check_rooms()
				hotel.guest_fun()
			elif int(x)==2:
				hotel.price_service()
			elif int(x)==3:
				hotel.enter()
		else:
			print('\nINVALID INPUT...\n')
			hotel.guest_fun()



	# def room_details():
	# def update_room():
	# def delete_details():
	# def login()
	# def services()


class guest_detail:
	def guest_name():
		print('PLEASE ENTER YOUR DETAILS\n')
		global name				
		name = input("FULLNAME = ")
		if fullname_re.fullmatch(name)==None:
			print("\t\t----INVALID NAME----\n")
			guest_detail.guest_name()
		else:
			return name

	def guest_address():
		global address
		address=input('ADDRESS = ')

	def guest_phn():
		global phn
		phn=input('PHONE NO. (XXXXXXXXXX)= ')
		if phn_no_re.fullmatch(phn)==None:
			print("\t\t----INVALID PHONE NO.----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			guest_detail.guest_phn()
		else:
			return phn

	def guest_email():
		global email
		email=input('EMAIL = ')
		if email_re.fullmatch(email)==None:
			print("\t\t----INVALID EMAIL----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			guest_detail.guest_email()
		else:
			return email

	def guest_aadhaar():
		global aadhaar
		aadhaar=input('AADHAAR NO. (XXXX XXXX XXXX) = ')
		if aadhaar_re.fullmatch(aadhaar)==None:
			print("\t\t----INVALID AADHAAR NO.----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			print('EMAIL =',email)
			guest_detail.guest_aadhaar()
		else:
			return aadhaar

	def guest_dtfrom():
		global datefrom
		datefrom=input('DATE OF ARRIVAL (YYYY-MM-DD) = ')
		if date_re.fullmatch(datefrom)==None:
			print("\t\t----INVALID DATE----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			print('EMAIL =',email)
			guest_detail.guest_dtfrom()
		else:
			return datefrom

	def guest_dtto():
		global dateto
		dateto=input('DATE OF DEPARTURE (YYYY-MM-DD) = ')
		if date_re.fullmatch(dateto)==None or dateto<datefrom:
			print("\t\t----INVALID DATE----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			print('EMAIL =',email)
			print('DATE OF ARRIVAL =',datefrom)
			guest_detail.guest_dtto()
		else:
			return dateto

	def guest_timefrom():
		global timefrom
		timefrom=input('TIME OF ARRIVAL (HH:MM(AM|PM)) = ')
		if time_re.fullmatch(timefrom)==None:
			print("\t\t----INVALID TIME----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			print('EMAIL =',email)
			print('DATE OF ARRIVAL =',datefrom)
			print('DATE OF DEPARTURE =',dateto)
			guest_detail.guest_timefrom()
		else:
			return timefrom

	def guest_timeto():
		global timeto
		timeto=input('TIME OF DEPARTURE (HH:MM(AM|PM)) = ')	
		if (time_re.fullmatch(timeto)==None) or (timefrom>=timeto and datefrom==dateto) :
			print("\t\t----INVALID TIME----\n")
			print('FULLNAME =',name)
			print('ADDRESS =',address)
			print('PHONE NO. =',phn)
			print('EMAIL =',email)
			print('DATE OF ARRIVAL =',datefrom)
			print('DATE OF DEPARTURE =',dateto)
			print('TIME OF ARRIVAL =',timefrom)
			guest_detail.guest_timeto()
		else:
			return timeto



def entry(price):
	guest_detail.guest_name()
	guest_detail.guest_address()
	guest_detail.guest_phn()
	guest_detail.guest_email()
	guest_detail.guest_aadhaar()
	guest_detail.guest_dtfrom()
	guest_detail.guest_dtto()
	guest_detail.guest_timefrom()
	guest_detail.guest_timeto()

	x=cur.execute(check_price,(price,))
	room_alloted=list(x)[0][0]
	if room_alloted:
		status=1
	print('\nROOM ALLOTED -->',room_alloted)
	
	try:
		cur.execute(update_room,(status,name,address,phn,email,aadhaar,datefrom,dateto,timefrom,timeto,room_alloted))
	except Exception:
		pass
	hotel.guest_fun()


#-------------------- MAIN PAGE FUNCTION --------------------#


hotel.enter()

conn.commit()
conn.close()