import time, subprocess, os, zipfile
import wmi
import pyperclip
import keyboard


weapon_list = [
    'i_giveitem smg02:camo04',
    'i_giveitem sr03:afro01',
    'i_giveitem ar22:pink02',
]


def til():
        
    keyboard.press_and_release('alt + tab')
    

    
def write():
    
    keyboard.write('wasa')


pyperclip.copy('exec py')
pyperclip.paste()

til()
time.sleep(0.8)
write()
