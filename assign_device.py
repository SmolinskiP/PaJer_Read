import mysql.connector as database
from db_connect import * #Connection data
from tkinter import *
from datetime import datetime
import sys
import serial
import os
from time import strftime

#Set required variables
actual_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
card_id = sys.argv[1]
device_id = sys.argv[2]
ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.2)
var_z_dupy = 69
#______________________________________________________________________________________

#Try to establish connection to database
try:
    conn = database.connect(
        user = dbLogin,
        password = dbPassword,
        host = dbHost,
        database = dbDatabase
    )
except database.Error as e:
    f = open(os.getcwd() + "\log\dbconnect.txt", "a")
    f.write(actual_time + ": " + f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
    f.close()
    var_z_dupy = 3
#______________________________________________________________________________________

print(device_id)
print(card_id)

#Get employee data
try:
    get_employee_fname = conn.cursor()
    get_employee_fname.execute("SELECT fname FROM employees WHERE cardid='%s'" % card_id)
    employee_fname = get_employee_fname.fetchall()[0][0]
    get_employee_lname = conn.cursor()
    get_employee_lname.execute("SELECT lname FROM employees WHERE cardid='%s'" % card_id)
    employee_lname = get_employee_lname.fetchall()[0][0]
    get_employee_id = conn.cursor()
    get_employee_id.execute("SELECT id FROM employees WHERE cardid='%s'" % card_id)
    employee_id = get_employee_id.fetchall()[0][0]
except:
    if var_z_dupy != 3:
        var_z_dupy = 1

#Get device data
try:
    get_device_id = conn.cursor()
    get_device_id.execute("SELECT id FROM devices WHERE sticker='%s'" % device_id)
    device_iddb = get_device_id.fetchall()[0][0]
    get_device_sn = conn.cursor()
    get_device_sn.execute("SELECT sn FROM devices WHERE sticker='%s'" % device_id)
    device_sn = get_device_sn.fetchall()[0][0]
except:
    if var_z_dupy != 3:
        var_z_dupy = 2

second_window = Tk()
second_window.resizable(True, True)
second_window.title('Summary')

#Create error window labels
if var_z_dupy == 1:
    no_employee_error_window = Label(second_window, text="Error 33:\nnie znaleziono\npracownika w bazie")
    no_employee_error_window.place(relx=0.5, rely=0.5, anchor='c')
elif var_z_dupy == 2:
    no_device_error_window = Label(second_window, text="Error 48:\nnie znaleziono\nurządzenia w bazie")
    no_device_error_window.place(relx=0.5, rely=0.5, anchor='c')
elif var_z_dupy == 3:
    no_dbconnection_error_window = Label(second_window, text="Error 51:\nnie można połączyć\nz bazą danych")
    no_dbconnection_error_window.place(relx=0.5, rely=0.5, anchor='c')
elif var_z_dupy == 69:
    #Create success window label
    print_employee_name = Label(second_window, text="Przypisano urządzenie " + device_sn)
    print_employee_name.place(relx=0.5, rely=0.4, anchor='c')
    print_employee_card_id = Label(second_window, text="Do pracownika " + employee_fname + " " + employee_lname)
    print_employee_card_id.place(relx=0.5, rely=0.6, anchor='c')
else:
    wtf_error_window = Label(second_window, text="Error 666:\nStało się coś\ndziwnego")
    wtf_error_window.place(relx=0.5, rely=0.5, anchor='c')

second_window.after(5000, lambda: second_window.destroy())
second_window.mainloop()
conn.close()