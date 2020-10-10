#!/usr/bin/env python
from timer import Timer
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

try:
    while True:
        # Put all below in this
        try:
            lcd.clear()
            #Possibly redundant if the cid variable also displays the Class ID prompt
            #lcd.message("Please enter a Class ID")
            cid = input("Please enter a Class ID:\n")

            lcd.clear()
            
            if len(cid) >=1: #If the input is not empty, check database
                db = mysql.connector.connect(
                host="10.0.0.240",
                user="attendanceadmin",
                passwd="Password01",
                database={cid}
                )

                cursor = db.cursor()
                reader = SimpleMFRC522()
                #Start the timer for timeout
                t = Timer.start()
            
                # Need to make the below time out after 1 hour --- i think it is set
                while t < 3600: #Timeout set to 1 hour
                    lcd.clear()
                    lcd.message('Place Card to\nrecord attendance')
                    id, text = reader.read()

                    cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
                    result = cursor.fetchone()

                    lcd.clear()

                    if cursor.rowcount >= 1:
                        lcd.message("Welcome " + result[1])
                        cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
                        db.commit()
                    else:
                        lcd.message("User does not exist.")
                        time.sleep(2)
            else: #No Class ID input
                lcd.message("No input detected")
        except:
            lcd.message("Error with input.")
except:
    lcd.message("Error, please try again")
finally:
    GPIO.cleanup()
