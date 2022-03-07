
import serial
import os
from time import strftime
from tkinter import *

ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)

clock_window = Tk()
clock_window.title('Clock')

def time():
    if ser.isOpen() == False:
        ser.open()

    string = "\nPrzyłóż kartę\n" + strftime('   %H:%M:%S')
    lbl.config(text = string)
    lbl.after(1000, time)
    
    if (ser.inWaiting() > 3):
        card_id = ser.readline()
        card_id = str(card_id)[3:14]
        print(card_id + '\n')
        ser.close()
        os.system("python3 read_device.py " + card_id)

img = PhotoImage(file=os.getcwd() + '\img\pp.png')
lbl = Label(clock_window, image=img, compound='top', font = ('calibri', 45, 'bold'))
lbl.pack(anchor = 'center')

time()

clock_window.mainloop()
