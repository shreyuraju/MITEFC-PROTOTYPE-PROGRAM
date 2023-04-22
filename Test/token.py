import drivers
from time import sleep
import time

disp = drivers.Lcd()

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

while True:
    tk= getToken()
    disp.lcd_clear()
    disp.lcd_display_string(str(tk),1)
    #sleep(1)
    #disp.lcd_display_string(str(t3),2)
    time.sleep(1)
