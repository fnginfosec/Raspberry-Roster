#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import Adafruit_CharLCD as LCD

try:
    while True:
        # Put all below in this
        try:
            lcd.clear()
            lcd.message("Please enter a Class ID")
            cid = input("Please enter a Class ID:\n")

            lcd.clear()

        db = mysql.connector.connect(
            host="10.0.0.240",
            user="attendanceadmin",
            passwd="Password01",
            database={cid}
        )

        cursor = db.cursor()
        reader = SimpleMFRC522()
        t_end = time.time() 60 * 5

        lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);
        # Need to make the below time out after 1 hour --- i think it is set
        try:
            while time.time() < t_end:
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
finally:
  GPIO.cleanup()