from threading import Thread, Event
from PIL import Image, ImageGrab

import win32api
import win32con
import win32gui
import ttkbootstrap as ttk
import pytesseract
import os
from ttkbootstrap.dialogs import Messagebox
import time
from pynput import keyboard
from firebase_init import Fb
from mob import Mob
from area_overlay import AreaOverlay
from radar import Radar
import pyautogui




root = ttk.Window(themename='darkly')
saved_area_val = ttk.StringVar()

mob = Mob(x1=0, x2=0, y1=0, y2=0)
radar = Radar(x1=0, x2=0, y1=0, y2=0, isRunning=False)

isRunning=False
area_overlay = AreaOverlay()
t_skill_order = ttk.StringVar()
     
    
def getRadarArea():
    area = area_overlay.runGame()
    setRadarArea(area[0], area[1], area[2], area[3])


def getMobArea():
    area = area_overlay.runGame()
    setMobArea(area[0], area[1], area[2], area[3])


def setRadarArea(x1,y1,x2,y2):
    radar.x1 = x1
    radar.y1 = y1
    radar.x2 = x2
    radar.y2 = y2
    radar.isRunning = False

def setMobArea(x1,y1,x2,y2):
    mob.x1 = x1
    mob.y1 = y1
    mob.x2 = x2
    mob.y2 = y2

def parseSkillOrder(): 
    skill_list = []   
    value = t_skill_order.get().replace(" ", "").replace(",","")    
    for i in range(len(value)):
        skill_list.append(value[i])
    return skill_list    

event= Event()
thread: Thread
def runFarm():
    radar.isRunning = True
    thread = Thread(target=processFarm)
    thread.start()


def stopFarm():
    radar.isRunning=False
    event.set()    

listener = keyboard.Listener(
    on_press=stopFarm())
listener.start()

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    

    

def processFarm():
    skills = parseSkillOrder()
    sectionWidht =int((radar.x2-radar.x1)/2)
    sectiongHeight = int((radar.y2-radar.y1)/4)                                                                        
    x=int(radar.x1+sectionWidht-(radar.x1+sectionWidht-radar.x1)/2)
    y=int(radar.y1+(sectiongHeight/2))
    while radar.isRunning:        
        click(x, y)        
        for i in skills:
            pyautogui.press(i)  
            time.sleep(1) 
        time.sleep(5) 

root.title('TL Farmer')
root.geometry('760x250')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

select_area_frame = ttk.Frame(root)
selectMobAreaLabel = ttk.Label(master=select_area_frame, text='Select radar area',font="Arial 12")
selectMobAreaLabel.grid(row=0, column=0, sticky='w')
selectMobButton = ttk.Button(master=select_area_frame, text="Select",
    command=getRadarArea,
    style='Outline.TButton',
    width=20
    ) 
selectMobButton.grid(row=0, column=1, sticky="e", padx=10)
select_area_frame.grid(row=0, column=0, sticky='nswe', pady=15,padx=10)   


select_mob_area_frame = ttk.Frame(root)
selectMobAreaLabel = ttk.Label(master=select_mob_area_frame, text='Select mob area ',font="Arial 12")
selectMobAreaLabel.grid(row=0, column=0, sticky='w')
selectMobButton = ttk.Button(master=select_mob_area_frame, text="Select",
    command=getMobArea,
    style='Outline.TButton',
    width=20
    ) 
selectMobButton.grid(row=0, column=1, sticky="e", padx=10)
select_mob_area_frame.grid(row=1, column=0, sticky='nswe', pady=15, padx=10)  

skill_oder_label = ttk.Label(master=root, text='Enter skill order unsing ''","(optional)' ,font="Arial 12")
skill_order = ttk.Entry(master=root, textvariable=t_skill_order, width=50)
skill_order.grid(row=3, column=0, sticky='w', padx=10)

ttk.Style().configure("Stop.TButton", padding=6, relief="flat",
   background="#BE3144",font="Arial 12", foreground='#ffffff')

ttk.Style().configure("Outline.TButton",  foreground='#ffffff',
                      padding=6, font="Arial 12",)

start_label = ttk.Label(master=root, text='Start farm after selection both areas and skill order(optional)' ,font="Arial 11")
start_label.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)
start_farm = ttk.Button(master=root, width=30, text='Start farm', style='Outline.TButton', command=runFarm)
start_farm.grid(row=1, column=1, sticky='nswe', padx=10, pady=10)
start_farm = ttk.Button(master=root, width=30, text='Stop farm', style='Stop.TButton', command=stopFarm)
start_farm.grid(row=2, column=1, sticky='nswe', padx=10, pady=10,)
skill_oder_label.grid(row=2, column=0, pady=10, sticky='w', padx=10)

def legal_check():
    fb = Fb()
    isCanAccess = fb.init_and_check()
    print("checking.....")
    return isCanAccess==False

if(legal_check()==True):
    exit()
else:    
    root.mainloop()