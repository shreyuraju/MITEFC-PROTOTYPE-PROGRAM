#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522
import signal
import binascii
from datetime import datetime
import drivers
from time import sleep
import time

import serial

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore

cred = credentials.Certificate("mite-fc-firebase-adminsdk-afnux-08b41329a0.json")

firebase_admin.initialize_app(cred,{'databaseURL':'https://mite-fc-default-rtdb.asia-southeast1.firebasedatabase.app'})

display = drivers.Lcd()

p=serial.Serial('/dev/ttyAMA0',9600)

continue_reading = True

NFCUID=""

NFCUSN=""

mealsAmt = 0

token =""

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

# This loop keeps checking for RFID tags
def checkUID() :
    display.lcd_clear()
    
    display.lcd_display_string("WELCOME",1)
    display.lcd_display_string("TAP YOUR ID",2)
    
    while continue_reading:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print ("Card detected")
            display.lcd_clear()
            display.lcd_display_string("CARD DETECTED",1)
            display.lcd_display_string("PLEASE HOLD",2)
            sleep(1)
            

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, print it
        if status == MIFAREReader.MI_OK:
            #print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
            if uid == [0,0,0,0]:
                print ("Card detected")
                display.lcd_clear()
                display.lcd_display_string("EMPTY TAG",1)
                display.lcd_display_string("PLEASE REGISTER",2)
                sleep(1)
            else :
                uidBlock =  [uid[0], uid[1], uid[2], uid[3]]
                uidHex = binascii.hexlify(bytes(uidBlock)).decode('utf-8')
                return uidHex.upper()

def getMealsAmt():
    ref = db.reference('admin').child('mealsAmt')
    mealsAmtData = ref.get()
    return mealsAmtData['amount']
            
def checkUser(NFCUID):
    display.lcd_clear()
    display.lcd_display_string("CHECKING USER",1)
    
    firestoreDB = firestore.client()
    users = firestoreDB.collection('users').document(NFCUID)
    doc = users.get()
    if doc.exists:
        print(f'{doc.id}=>{doc.to_dict()}')
        data=doc.to_dict()
        display.lcd_clear()
        display.lcd_display_string("USER FOUND",1)
        display.lcd_display_string(data["USN"],2)
        sleep(1)
        NFCUSN = data["USN"]
        print(NFCUSN)
        global mealsAmt
        mealsAmt = getMealsAmt()
        getBalance(NFCUSN)
    else :
        print('User NOT Found')
        display.lcd_clear()
        display.lcd_display_string("USER NOT FOUND",1)
        sleep(1)
        return

def getBalance(NFCUSN):
    ref = db.reference('users').child(NFCUSN)
    data = ref.get()
    bal = data['balance']
    
    if bal==0 :
        display.lcd_clear()
        display.lcd_display_string("EMPTY WALLET",1)
        sleep(1)
        print("No Balance")
    elif bal<mealsAmt :
        display.lcd_clear()
        display.lcd_display_string("NOT ENOUGH BALANC",1)
        display.lcd_display_string("YOUR BAL IS : "+str(bal),2)
        sleep(1)
        print("Not enough Balance")
    else :
        newBalance = bal - mealsAmt
        addTransaction(NFCUSN, mealsAmt, newBalance)
            
def updateNewBalance(NFCUSN, newBalance):
    ref = db.reference('users').child(NFCUSN)
    data = {'balance':newBalance}
    done = ref.update(data)
    #display.lcd_clear()
    #display.lcd_display_string("NEW BALANCE UPD",1)
    #display.lcd_display_string("ATED "+NFCUSN,2)
    print("New Balance Updated " +NFCUSN)

def getCurrentTime():
    now = datetime.now()
    currentTime = now.strftime("%Y/%m/%d %H:%M:%S")
    utrTime = now.strftime("%Y%m%d%H%M%S")
    dt = now.strftime("%Y%m%d")
    return currentTime, utrTime, dt
    
def getUtr(NFCUSN):
    time, utrTime, dt = getCurrentTime()
    utr = NFCUSN+utrTime
    return time, utr, dt        
    
def addTransaction(NFCUSN, mealsAmt, newBalance):
    date, utr, dt = getUtr(NFCUSN)
    data = {
        "USN":NFCUSN,
        "amount":mealsAmt,
        "date":date,
        "mode":"debit",
        "utr":utr
    }
    ref = db.reference('admin').child('alltransaction')
    done = ref.push().set(data)
    updateNewBalance(NFCUSN, newBalance)
    display.lcd_clear()
    display.lcd_display_string("PRINTING TOKEN",1)
    display.lcd_display_string("BALANCE : "+str(newBalance),2)
    sleep(1)
    printToken(NFCUSN, mealsAmt, date, utr, dt)

t3=0
t2=0
t1=0
I=0

def getToken():
    global t3,t2,t1,I
    I+=1
    if t3<9 :
        t3=I
    if I>9 :
        I-=10
        t2+=1
        t3-=9
    if t2>9 :
        t2-=10
        t1+=1
    tk=str(t1)+str(t2)+str(t3)
    return tk
   
def eT(text):
    return text.encode('utf-8')
    
def printToken(NFCUSN, mealsAmt, date, utr, dt):
    mealsAmt="Meals : Rs. "+str(mealsAmt)
    utr="UTR : "+utr
    global token
    tkn= getToken()
    
    p.write(b'\x1B\x40')
    
    #PRINTING FORMAT
    p.write(b'\n\n')
    p.write(b'\x1B\x61\x01') # Define the command to center justify the text.
    p.write(b'\x1B\x21\x34') #increase the font size.
    p.write(b'\x1B\x45\x02') # Turn bold font on.
    p.write(eT("MITE"))
    p.write(b'\n')

    #
    token ="TOKEN NO :"+tkn
    
    p.write(b'\x1B\x21\x10') #Set the font size
    p.write(b'\x1B\x45\x02') # Turn bold font on.
    p.write(eT(token))

    #
    p.write(b'\n')
    p.write(b'\x1B\x61\x01') #center justify 
    p.write(b'\x1B\x21\x00') # Set the font size
    p.write(b'\x1B\x45\x02') # Turn bold font on.
    p.write(eT(utr))

    #
    p.write(b'\n')
    p.write(b'\x1B\x61\x01') #center justify 
    line2 = date+" "+NFCUSN
    p.write(eT(line2))

    #
    p.write(b'\n')
    p.write(b'\x1B\x61\x01') #center justify 
    p.write(b'\x1B\x21\x34') #increase the font size
    p.write(b'\x1B\x21\x10')
    p.write(eT(mealsAmt))

    # Feed the paper and cut it.
    p.write(b'\n\n\n\n\x1D\x56\x41\x30') # Feed three lines and cut the paper.
    updateTokenCnt(tkn, dt)
    #p.close()
    return
    
def updateTokenCnt(token, dt) :
    ref = db.reference('admin').child("token_count").child(dt)
    data = {'date':dt,'token_count':token}
    done = ref.update(data)
    return
    
while True:
    
    NFCUID=checkUID()
    print(NFCUID)
    checkUser(NFCUID)
    
    time.sleep(3)
