from threading import Thread, Event
import win32api
import win32con
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
import time
from pynput import keyboard
from PIL import  ImageGrab
from firebase_init import Fb
from mob import Mob
from area_overlay import AreaOverlay
from radar import Radar
import pyautogui
import os
import pytesseract
import cv2
import sys
import numpy as np
import re
from farm_status import FStatus
import atexit
from cacher import Cacher


root = ttk.Window(themename='darkly')
saved_area_val = ttk.StringVar()

mob = Mob(x1=0, x2=0, y1=0, y2=0, last_status="")
radar = Radar(x1=0, x2=0, y1=0, y2=0, isRunning=False)
f_status = FStatus(is_stuck=False, last_status="", status_count=0)


isRunning=False
area_overlay = AreaOverlay()
t_skill_order = ttk.StringVar()
is_stuck = False     
    
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
    

current_directory = os.getcwd()

def replace_except_symbols_and_numbers(input_string):
    # Replace all characters except ., /, numbers with an empty string
    result = re.sub(r'[^0-9./]', '', input_string)
    return result


def check_colors():
    # Load the image
    image = cv2.imread(f"{current_directory}\screenshot.png")

    # Convert the image to RGB (from BGR, which is OpenCV's default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the specific colors to check
    color_1 = np.array([247, 194, 66], dtype=np.uint8)  # #F7C242
    color_2 = np.array([210, 126, 87], dtype=np.uint8)  # #DE6128
    color_3 = np.array([255, 110, 44], dtype=np.uint8)  # #FF6E2C

    # Create masks for the specific colors
    mask_color_1 = cv2.inRange(image_rgb, color_1, color_1)
    mask_color_2 = cv2.inRange(image_rgb, color_2, color_2)
    mask_color_3 = cv2.inRange(image_rgb, color_3, color_3)

    # Check if any pixel in the image matches the colors
    contains_color_1 = np.any(mask_color_1)
    contains_color_2 = np.any(mask_color_2)
    contains_color_3 = np.any(mask_color_3)

    return contains_color_1, contains_color_2, contains_color_3

def check_is_contains():
    contains_color_1, contains_color_2, contains_color_3 = check_colors()
    if contains_color_1:
        # print("Only color #F7C242 is present in the image.")
        return True
    elif contains_color_2:
        # print("Only color #D27E57 is present in the image.")
        return True
    elif contains_color_3:
        # print("Only color #FF6E2C is present in the image.")
        return True
    else:
        # print("Neither color #F7C242 nor #DE6128 nor FF6E2C is present in the image.")
        return False




def get_mob_hp():
    im = ImageGrab.grab(bbox=(mob.x1, mob.y1, mob.x2, mob.y2))
    im.save("screenshot_mob.png")  
    img = cv2.imread(f"{current_directory}\screenshot_mob.png")
    lower_bound = np.array([150, 130, 150], dtype=np.uint8)
    upper_bound = np.array([255, 255, 255], dtype=np.uint8)

    # Create a mask that identifies the white areas
    white_mask = cv2.inRange(img, lower_bound, upper_bound)

    # Invert the mask to cover non-white areas
    non_white_mask = cv2.bitwise_not(white_mask)

    # Turn all non-white areas to black
    result_image = cv2.bitwise_and(img, img, mask=white_mask)
    imageText = pytesseract.image_to_string(image=result_image, lang='eng', config="--psm 6").replace("\n", "").replace(" ","") 
    return replace_except_symbols_and_numbers(imageText)


def reset_status():    
    f_status.is_stuck=False
    f_status.last_status=""
    f_status.status_count=0

def search_mob_in_radar():
    sectionWidht =int((radar.x2-radar.x1)/2)
    sectiongHeight = int((radar.y2-radar.y1)/4)   
    number_section = int(sectionWidht/5)
    for i in range(3):       
        if f_status.is_stuck:
            reset_status()
            continue
        im = ImageGrab.grab(bbox=(radar.x1+number_section, radar.y1+(sectiongHeight*i),radar.x1+sectionWidht, radar.y1+sectiongHeight*(i+1)))            
        im.save("screenshot.png")
        isContains = check_is_contains()
        if isContains:
            x= radar.x1+(sectionWidht/2)-number_section
            y= radar.y1+(sectiongHeight/2) +sectiongHeight*(i)           
            return int(x),int(y)
        
    for j in range(3):
        im = ImageGrab.grab(bbox=(radar.x1+sectionWidht+number_section, radar.y1+(sectiongHeight*j),radar.x2, radar.y1+sectiongHeight*(j+1)))            
        im.save("screenshot.png")
        isContains = check_is_contains()
        if isContains:
            x= sectionWidht+(sectionWidht/2)-number_section
            y= radar.y1+(sectiongHeight/2) +sectiongHeight*(j)

            return int(x),int(y)
    return(0,0)    
        
def check_mob_hp():
    result_text =  get_mob_hp()
    return result_text
    pass

def skill_cycle(skills: list):  
    for i in skills:
        if(check_mob_hp()!=""):
            pyautogui.press(i)  
            time.sleep(1)
        else:
            return        

def save_config():
    caher = Cacher()
    caher.save_data_to_file(instance1=mob, instance2=radar, skills=t_skill_order.get())
    pass

def restore_config():
    caher = Cacher()
    instance1, instance2, skills = caher.load_data_from_file()
    t_skill_order.set(skills)
    mob.__dict__=instance1.__dict__.copy()
    radar.__dict__=instance2.__dict__.copy()    


def processFarm():
    skills = parseSkillOrder() 
                                                                   
    while radar.isRunning:
        mob_status = check_mob_hp()        
        if mob_status!="" and f_status.is_stuck==False:
            if(f_status.last_status==mob_status):
                f_status.status_count+=1
            f_status.last_status=mob_status
            if(f_status.status_count>3):
                f_status.is_stuck=True    
            skill_cycle(skills)
            continue        
        x,y = search_mob_in_radar()
        if(x==0 & y==0):
            continue
        click(x, y)        
        skill_cycle(skills)

root.title('TL Farmer')
root.geometry('760x300')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

ttk.Style().configure('Main.TButton',
                background='#6200EA',    # Orange material color
                foreground='white',      # Text color
                borderwidth=1,           # Border width
                relief='flat',             # Border style (flat to match material design)
                font=('Helvetica', 12))  # Font style and size

# Change the style of the button on hover
ttk.Style().map('Main.TButton',
          background=[('hover', '#E64A19')], # Darker orange for hover effect
          foreground=[('hover', 'white')])


select_area_frame = ttk.Frame(root)
selectMobAreaLabel = ttk.Label(master=select_area_frame, text='Select radar area',font="Arial 12", width=15)
selectMobAreaLabel.grid(row=0, column=0, sticky='w')
selectMobButton = ttk.Button(master=select_area_frame, text="Select",
    command=getRadarArea,
    style='Main.TButton',
    width=19
    ) 
selectMobButton.grid(row=0, column=1, sticky="e", padx=10)
select_area_frame.grid(row=0, column=0, sticky='nswe', pady=15,padx=10)   



select_mob_area_frame = ttk.Frame(root)
selectMobAreaLabel = ttk.Label(master=select_mob_area_frame, text='Select mob area ',font="Arial 12" , width=15)
selectMobAreaLabel.grid(row=0, column=0, sticky='w')
selectMobButton = ttk.Button(master=select_mob_area_frame, text="Select",
    command=getMobArea,
    style='Main.TButton',
    width=19,       
    ) 
selectMobButton.grid(row=0, column=1, sticky="e", padx=10)
select_mob_area_frame.grid(row=1, column=0, sticky='nswe', pady=15, padx=10)  

skill_oder_label = ttk.Label(master=root, text='Enter skill order separated ''","' ,font="Arial 12")
skill_order = ttk.Entry(master=root, textvariable=t_skill_order, width=55)
skill_order.grid(row=3, column=0, sticky='w', padx=10)

ttk.Style().configure('Save.TButton', padding=6, relief="flat",background="#2979FF",font="Arial 12", foreground='#ffffff')
ttk.Style().map('Save.TButton',background=[('hover', '#039BE5')])
config_frame=ttk.Frame(root)
save_conf = ttk.Button(master=config_frame, text="Save config",
    command=save_config,
    width=16,
    style='Save.TButton',
    )
ttk.Style().configure('Restore.TButton', padding=6, relief="flat",background="#4CAF50",font="Arial 12", foreground='#ffffff')
ttk.Style().map('Restore.TButton',background=[('hover', '#00C853')])

save_conf.grid(row=0, column=0, sticky='nswe', padx=10)
rest_conf = ttk.Button(master=config_frame, text="Restore config",
    command=restore_config,
    width=16,
    style='Restore.TButton',
    )
rest_conf.grid(row=0, column=1, sticky='w', padx=10)
config_frame.grid(row=4, column=0, sticky='nswe', pady=15)

ttk.Style().configure("Stop.TButton", padding=6, relief="flat",
   background="#BE3144",font="Arial 12", foreground='#ffffff')
ttk.Style().map('Stop.TButton',
                background=[('hover', '#F50057')])

ttk.Style().configure('Start.TButton',
                background='#4CAF50',    
                foreground='white',     
                borderwidth=1,          
                relief='flat',            
                font=('Helvetica', 12))  

ttk.Style().map('Start.TButton',
          background=[('hover', '#1B5E20')], 
          foreground=[('hover', 'white')])

start_label = ttk.Label(master=root, text='Start farm after selection both areas and skill order' ,font="Arial 11", wraplength=300, anchor='center')
start_label.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)
start_farm = ttk.Button(master=root, width=30, text='Start farm', style='Start.TButton', command=runFarm)
start_farm.grid(row=1, column=1, sticky='nswe', padx=10, pady=10)
start_farm = ttk.Button(master=root, width=30, text='Stop farm', style='Stop.TButton', command=stopFarm)
start_farm.grid(row=2, column=1, sticky='nswe', padx=10, pady=10,)
skill_oder_label.grid(row=2, column=0, pady=10, sticky='w', padx=10)



if getattr(sys, 'frozen', False):
    # Get the directory where the .exe is located
    base_dir = os.path.dirname(sys.executable)
else:
    # Use the directory of the script
    base_dir = os.path.dirname(__file__)

log_file_path = os.path.join(base_dir, "output_log.txt")
log_file = open(log_file_path, "a")


# Redirect stdout and stderr to the log file, and flush after every write
class Logger:
    def __init__(self, file):
        self.terminal = sys.stdout
        self.log = file

    def write(self, message):
        # Write to terminal and log file
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()  # Ensure each write is flushed to file immediately

    def flush(self):
        pass  # flush method is needed for compatibility with Python's `sys.stdout`
    
sys.stdout = Logger(log_file)
sys.stderr = Logger(log_file)


def on_exit():
    log_file.close()


print("started")

atexit.register(on_exit)

def legal_check():
    fb = Fb()
    isCanAccess = fb.init_and_check()
    return isCanAccess==False


if(legal_check()):
    exit()
else:    
    root.mainloop()