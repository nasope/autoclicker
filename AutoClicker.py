from glob import glob
from multiprocessing.connection import wait
import tkinter as tk
from tkinter import ttk
import time as t
import keyboard
import json
import random
import win32api, win32con

randomtime = 1
time = 1
hotkey = "a"

#scheme
primary = "#2c3333"
secondary = "#395b64"
tertiary = "#e7f6f2"
font = "Consolas"

#main window
window = tk.Tk()
window.title("AutoClicker v1.0")
window.resizable(False, False)
window.geometry("300x250")
window.configure(background=primary)

togglevar = tk.IntVar()

# top widget
top = tk.Frame(window,width = 300, height = 100, background=secondary)
title = ttk.Label(top, text="AutoClicker", font=(font, 25), background=secondary, foreground=tertiary)
title.place(anchor="center", relx=0.5, rely=0.5)
author = ttk.Label(top, text="Created by: N.S Pedersen", font=(font, 10), background=secondary, foreground=tertiary)
author.place(anchor="center", relx=0.5, rely=0.8)
top.place(anchor="center", relx=0.5, rely=0.1)

# bottom widget
bottom = tk.Frame(window,width = 300, height = 250, background=secondary)
bottom.place(anchor="center", relx=0.5, rely=0.815)

info = ttk.Label(bottom, text="Emergency stop: 'ctrl+shift+o'", font=(font, 9), background=secondary, foreground=tertiary)
info.place(anchor="center", relx=0.5, rely=0.07)

timeinterval = ttk.Label(bottom, text="Delay:", font=(font, 10), background=secondary, foreground=tertiary)
timeinterval.place(anchor="center", relx=0.25, rely=0.2)
timeinterval_entry = ttk.Entry(bottom, width=10, font=(font, 10), background=tertiary)
timeinterval_entry.place(anchor="center", relx=0.7, rely=0.2)

randominterval = ttk.Label(bottom, text="Random Delay", font=(font, 10), background=secondary, foreground=tertiary)
randominterval.place(anchor="center", relx=0.25, rely=0.3)
randominterval_entry = ttk.Entry(bottom, width=10, font=(font, 10), background=tertiary)
randominterval_entry.place(anchor="center", relx=0.7, rely=0.3)

inputmethod_label = ttk.Label(bottom, text="Input key", font=(font, 10), background=secondary, foreground=tertiary)
inputmethod_label.place(anchor="center", relx=0.25, rely=0.6)

inputmethod_button = tk.Button(bottom, text="", font=(font, 10), background=secondary, foreground=tertiary)
inputmethod_button.place(anchor="center", relx=0.7, rely=0.6)

def spam():
    global hotkey

    keyboard.remove_hotkey(hotkey)
    inputmethod_button.configure(text="Stop ("+str(hotkey)+")")
    randominterval_entry.configure(state="disabled")
    timeinterval_entry.configure(state="disabled")
    inputmethod_button.configure(state="disabled")

    temp = False
    if togglevar.get() == 1:
        temp = True


    toggle.configure(state="disabled")

    if temp == False:
        t.sleep(0.2)

    while keyboard.is_pressed(hotkey) == temp:
        a = int(time)
        b = int(random.randint(0, int(randomtime)))
        sum = a + b
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        t.sleep(sum/2000)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        t.sleep(sum/2000)

    inputmethod_button.configure(text="Start ("+str(hotkey)+")")
    randominterval_entry.configure(state="normal")
    timeinterval_entry.configure(state="normal")
    inputmethod_button.configure(state="normal")
    toggle.configure(state="normal")
    t.sleep(0.2)
    keyboard.add_hotkey(hotkey, spam)

def OnReturn(x):
    window.focus_set()
window.bind('<Return>', OnReturn)

def validate(event):
    focus = event.widget
    value = focus.get()

    if value.isnumeric() == False:
        focus.delete(0, "end")
        return False
    else:
        return True
        
def setrandominterval(event):
    global randomtime
    keyboard.remove_hotkey(hotkey)
    if validate(event):
        randomtime = event.widget.get()
        save()
    else:
        event.widget.insert(0, randomtime)
    keyboard.add_hotkey(hotkey, spam)

def settimeinterval(event):
    global time
    keyboard.remove_hotkey(hotkey)
    if validate(event):
        time = event.widget.get()
        save()
    else:
        event.widget.insert(0, time)
    keyboard.add_hotkey(hotkey, spam)


def save():
    with open('./config.json', 'w') as fp:
        json.dump({"time": time, "randomtime": randomtime, "hotkey": hotkey, "toggle": togglevar.get()}, fp)    
randominterval_entry.bind('<Return>', setrandominterval)
timeinterval_entry.bind('<Return>', settimeinterval)


def record():
    window.focus_set()
    global Onrecord
    global hotkey

    keyboard.remove_hotkey(hotkey)
    inputmethod_button.config
    inputmethod_button.configure(text="Recording...")
    key = keyboard.read_key()
    inputmethod_button.configure(text="Start ("+str(key)+")")
    hotkey = key
    Onrecord = False
    keyboard.add_hotkey(hotkey, spam)
    save()


toggle_label = ttk.Label(bottom, text="Toggle", font=(font, 10), background=secondary, foreground=tertiary)
toggle_label.place(anchor="center", relx=0.25, rely=0.45)
toggle = tk.Checkbutton(bottom, text="", background=secondary, foreground=primary, activebackground=secondary, activeforeground=tertiary, variable=togglevar, command=save)
toggle.place(anchor="center", relx=0.7, rely=0.45)

inputmethod_button.configure(command=record)

def load():
    global time
    global randomtime
    global hotkey
    global togglevar

    with open('./config.json', 'r') as fp:
        data = json.load(fp)
        time = data["time"]
        randomtime = data["randomtime"]
        togglevar.set(data["toggle"])

        hotkey = data["hotkey"]
        inputmethod_button.configure(text="Start ("+str(hotkey)+")")

        timeinterval_entry.insert(0, time)
        randominterval_entry.insert(0, randomtime)
        keyboard.add_hotkey(hotkey, spam)
    fp.close()
load()


def emergency():
    window.destroy()

keyboard.add_hotkey("ctrl+shift+o", emergency)

window.mainloop()
