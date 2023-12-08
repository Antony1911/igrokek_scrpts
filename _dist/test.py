import os
from os.path import abspath, split
from textwrap import wrap
from tkinter import Image
import PySimpleGUI as sg
import shutil
import PIL
import xml.etree.ElementTree as ET
from xml.dom import minidom
import wx
import subprocess
import os.path
import os
import random
import subprocess
from colorama import Style, Fore
import image
import cv2
import sys

# temp = "d:\\_WfPC_rep\\wfpc_work\\2022\\WFPC_Content_Pack_14\\14_6_March_Battle_Pass_Cheap_Skin_x6"
# #---------------------------------------------------------
# def get_Weapons():
#     path = temp + "\\Game\\Objects\\Weapons\\"
achieve = "challenge_badge_inoagent01_01"

text = """  <item name="f_sniper_fbs_saboteur01" regular=""/>
            <item name="sr56_saboteur01_shop" regular=""/>
            <item name="pt33_saboteur01_shop" regular=""/>
            <item name="kn43_saboteur01" regular=""/>
            <item name="sr56_saboteur01skin_shop" regular=""/>
            <item name="pt33_saboteur01skin_shop" regular=""/>
            <item name="kn43_saboteur01skin_shop" regular=""/>
            <item name="charm_saboteur01_shop" regular=""/>
            <item name="unlock_saboteur01_stripe" regular=""/>
            <item name="unlock_saboteur01_badge" regular=""/>
            <item name="unlock_saboteur01_mark" regular=""/>
            <item name="unlock_fbs_saboteur01_mark" regular=""/>"""


# def AskPath(): 
#     layout = [
#         [sg.Text(r"path to content", text_color="black")],
#         [sg.InputText(default_text = r"d:\\", key = "input")],
#         [sg.Output(key = "out")],
#         [sg.OK(key='OK'), sg.Cancel()]
#     ]

#     window = sg.Window(f'window', layout)

#     while True:
#         event, values = window.read(close=True)
#         # =========================
#         if event == 'OK':
#             # window["-ML-"].update()
#             # values["-ML-"] = values["-INPUT-"]
#             # continue
            

#         # =========================
#         if event in ('Cancel', None) or event == sg.WIN_CLOSED:
#             break
#     window.close()

# AskPath()
def ChatBot():
    layout = [[(sg.Text('This is where standard out is being routed', size=[40, 1]))],
              [sg.Output(size=(80, 20))],
              [sg.Multiline(size=(70, 5), enter_submits=True, key='out'),
               sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
               sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('Chat Window', layout, default_element_size=(30, 2))

    # ---===--- Loop taking in user input and using it to query HowDoI web oracle --- #
    while True:
        event, value = window.read()
        if event == 'SEND':
            print(value['out'])
        else:
            break
    window.close()



bundleItem_contentList = []
testSkin = "inoagent01"
iconsPath = "e:\\partner_WPC\\wfpc_mrg\\main\\Game\\Libs\\Icons\\"
# modString = f"""<item name="{searchingItem}" regular=""/>"""



for root, dirs, files in os.walk(iconsPath):
    for searchingItem in files:
        if testSkin in searchingItem and searchingItem.endswith('.tif'):
            searchingItem = searchingItem.split('.tif')[0]
            
            if 'charm' in searchingItem:
                searchingItem = searchingItem + "_shop"
                bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
            
            if "weapons_" in searchingItem:
                searchingItem = searchingItem.split('weapons_')[1]
                if "kn" in searchingItem.split('_')[0]:
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
                else:
                    searchingItem01 = searchingItem + "_shop"
                    searchingItem02 = searchingItem + "skin_shop"
                    
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem01}" regular=""/>""")
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem02}" regular=""/>""")

            if "badge" in searchingItem or "mark" in searchingItem:
                searchingItem = searchingItem.split('challenge_')[1]
                if "_fbs_" in searchingItem:
                    specialType = searchingItem.split('_fbs_')[0]
                    searchingItem = f"unlock_fbs_{testSkin}_{specialType}"
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")
                else:
                    specialType_01 = searchingItem.split('_')[0]
                    specialType_02 = searchingItem.split(specialType_01 + "_")[1]
                    searchingItem = f"unlock_{specialType_02}_{specialType_01}"
                    bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")

            if f"stripe_{testSkin}" in searchingItem:
                specialType = searchingItem.split("challenge_stripe_")[1]
                searchingItem = f"unlock_{specialType}_stripe"
                bundleItem_contentList.append(f"""\n\t\t\t<item name="{searchingItem}" regular=""/>""")



# for i in bundleItem_contentList: 
#     print(i)
print(bundleItem_contentList)
open("d:\\_WfPC_rep\\wfpc_work\\2022\\WFPC_Content_Pack_25\\25_1_April_PREMIUM_New_weapon_SMG_SAR_109T_Specs\\sss.xml", 'a')

with open("d:\\_WfPC_rep\\wfpc_work\\2022\\WFPC_Content_Pack_25\\25_1_April_PREMIUM_New_weapon_SMG_SAR_109T_Specs\\sss.xml", 'r+') as f:
    f.writelines(bundleItem_contentList)
    