#!/usr/bin/env python
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

# Connect to the MySql Database
db = mysql.connector.connect(
        host="10.0.0.240",
        user="attendanceadmin",
        passwd="Password01",
        database= "attendancesystem"
        ) 

def scanuser(db): #Record User data
    cursor = db.cursor()
    reader = SimpleMFRC522()
    
    ## Grab the Class ID input from keypad
    lcd.clear()
    lcd.message("Please enter a Class ID")
    cid = input("Please enter a Class ID:\n")
    
    if len(cid) >=1: #If the input is not empty, check database
        lcd.clear()
        lcd.message('Place Card to\nrecord attendance')
        id, text = reader.read()

        cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
        result = cursor.fetchone()

        lcd.clear()
        
        # Add the scanned card into SQL database
        if cursor.rowcount >= 1:
            lcd.message("Welcome " + result[1])
            cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
            db.commit()
        else:
            lcd.message("User does not exist.")
    else:
        lcd.message("No input\ndetected")

##################### Main #####################
try:
    while True:
        try:
            endtime = datetime.now() + timedelta(seconds=15) #Set timeout in seconds
            while datetime.now() < endtime:
                scanuser(db)
                time.sleep(2)
            if datetime.now() == endtime:
                break
        except:
            lcd.message("Error\nPanic!")
except:
    lcd.message("Error Occurred.")
                
finally:
    GPIO.cleanup()       
