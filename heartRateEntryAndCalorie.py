
from tkinter import *
from prettytable import PrettyTable
import re
import serial, os

table = PrettyTable()
table.field_names = ['First Name', 'Last Name', 'Calories Burned']


fields = 'First Name', 'Last Name', 'Age', 'Weight'
firstNames = []
lastNames = []
ageList = []
weightList = []

ser = serial.Serial('/dev/cu.usbmodem1411', 250000)

s1y = []
s2y = []
s1x = []
s2x = []
s1y.append(0)
s2y.append(0)
s1x.append(0)
s2x.append(0)

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      reg = root.register(correct)
      if (field == 'Age' or field == 'Weight'):
         ent.config(validate="key", validatecommand=(reg,'%P'))
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

def correct(inp):
   if inp.isdigit():
      return True
   elif inp =="":
      return True
   else:
      return False

def fetch(entries):
   count=0
   sex = v.get()
   for i in range(0,4):
      if entries[i][1].get()=="":
         popupmsg("All fields must be entered!")
         count+=1
   if count==0:
      firstNames.append(entries[0][1].get())
      lastNames.append(entries[1][1].get())
      ageList.append(float(entries[2][1].get()))
      weightList.append(float(entries[3][1].get()))
      for i in range(0,4):
         entries[i][1].delete(0, END)
      calcScore(ageList[-1], weightList[-1])
   update_sensor()


def calcScore(age, weight):
   i = 0
   sex = v.get()
   sensor = variable.get()
   sensorNum = sensor[-1]
   calories = 0
   if sensorNum == 1:
      data = s1y
   else:
      data = s2y
   if sex == 1:
      while i < len(data):
         calories += (-55.0969 + (0.6309*data[i])+(0.1988*weight)+(0.2017*age))/4.184
         i+=1
   elif sex == 2:
      while i < len(data):
         calories += (-20.4022 + (0.4472*data[i])+(0.1263*weight)+(0.074*age))/4.184
         i+=1
   if sensorNum == 1:
      s1y.clear()
   else:
      s2y.clear()
   table.add_row([firstNames[-1], lastNames[-1], calories])
   table.sortby = "Calories Burned"
   table.reversesort = True
   print(table)
    

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Error!")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Ok", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def update_sensor():
   data = ser.readline().decode()
   
   if len(data) > 7:
      sensorList = data.split(',')
      sensor1 = float(sensorList[0])
      sensor2 = float(sensorList[1])
      sensor2 = sensor2/4
      s1y.append(sensor1)
      s2y.append(sensor2)
   else: 
      data = ser.readline().decode()
      sensorList = data.split(',')
      sensor1 = float(sensorList[0])
      sensor2 = float(sensorList[1])
      sensor2 = sensor2/4
      s1y.append(sensor1)
      s2y.append(sensor2)
   return s1y, s2y

if __name__ == '__main__':
   root = Tk()
   T= Label(root, text="Please enter your information", font = "Verdana 16 bold")
   T.pack()

   ents = makeform(root, fields) 

   v = IntVar()
   Radiobutton(root, text="Male", padx=5, pady=5, variable=v, value=1).pack(anchor=W)
   Radiobutton(root, text="Female", padx=5, pady=5, variable=v, value=2).pack(anchor=W)

   variable = StringVar(root)
   variable.set("Sensor 1") # default value
   
   drop = OptionMenu(root, variable, "Sensor 1", "Sensor 2")
   drop.pack()

   b1 = Button(root, text='Submit',
          command=(lambda e=ents: fetch(e)))
   b1.pack(padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(padx=5, pady=5)
   
   update_sensor()

   root.mainloop()
   




