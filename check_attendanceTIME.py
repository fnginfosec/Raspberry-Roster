#!/usr/bin/env python
import time
import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

try:
    while True:
        
        lcd.clear()
        lcd.message("Please enter a\nClass ID")
        cid = input("Please enter a Class ID:")
        lcd.clear()

        #cid2 = "t" + cid
        db = mysql.connector.connect(
          host="10.0.0.240",
          user="attendanceadmin",
          passwd="Password01",
          database="attendancesystem"
        )

        cursor = db.cursor()
        reader = SimpleMFRC522()
        t_end = datetime.datetime.now() + datetime.timedelta(minutes=1)


        try:
          while datetime.datetime.now() < t_end:
            lcd.clear()
            lcd.message('Place Card to\nrecord attendance')
            if datetime.datetime.now() < t_end:
                id, text = reader.read()
            else:
                continue
            

            cursor.execute("Select id, name FROM users WHERE rfid_uid="+str(id))
            result = cursor.fetchone()

            lcd.clear()

            if cursor.rowcount >= 1:
                lcd.message("Welcome " + result[1])
                cursor.execute("INSERT INTO" + str(cid) + "(user_id) VALUES (%s)", (result[0],) )
                db.commit()
            else:
                lcd.message("User does not exist.")
            time.sleep(2)
        except:
            lcd.clear()
    lcd.clear()
finally:
    GPIO.cleanup()