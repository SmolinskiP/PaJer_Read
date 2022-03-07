from tkinter import * #GUI
import sys
import serial
import os
from time import strftime

#Set required variables
card_id = sys.argv[1]
ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=5)

#Create Main Window
mainWindow = Tk()
#mainWindow.geometry('300x200')
mainWindow.resizable(True, True)
mainWindow.title('Assign_Device')

def scan_device():
    if ser.isOpen() == False:
        ser.open()

    string = "Witaj\n" + strftime('%H:%M:%S')
    lbl.config(text = string)
    lbl.after(1000, scan_device)
    
    if (ser.inWaiting() > 3):
        device_id = ser.readline()
        device_id = str(device_id)[3:14]
        print(device_id + '\n')
        ser.close()
        os.system("python3 assign_device.py " + card_id + " " + device_id)

img = PhotoImage(file=os.getcwd() + '\img\pp.png')
lbl = Label(mainWindow, image=img, compound='top', font = ('calibri', 45, 'bold'))
lbl.pack(anchor = 'center')

scan_device()

mainWindow.after(5000, lambda: mainWindow.destroy())
mainWindow.mainloop()