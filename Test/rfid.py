#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522

# Hook the SIGINT
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
# Capture SIGINT for cleanup when the script is aborted
signal.signal(signal.SIGINT, end_read)
# Create an instance of the MFRC522 class
MIFAREReader = mfrc522.MFRC522()
while continue_reading:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")
            
            

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, print it
        if status == MIFAREReader.MI_OK:
            #print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            if uid == [0,0,0,0]:
                print ("Card detected")
                sleep(1)
            else :
                uidBlock =  [uid[0], uid[1], uid[2], uid[3]]
                uidHex = binascii.hexlify(bytes(uidBlock)).decode('utf-8')
                print(uidHex.upper())
