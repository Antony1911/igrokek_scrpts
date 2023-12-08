import os, glob
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os.path
from os import name, path
import PySimpleGUI as sg
import shutil
sg.theme('DarkGrey13')

#---------------------------------------------------------
def Ask_Path():

    layout = [
        [sg.Text("Insert your WFC/WFPC repo path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = r"e:\\wfpc-minsk\\Game",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.Text("Skin absolute path ('Game' folder)", text_color='yellow')],
        [sg.InputText(
            default_text = "Soul of the mind, key to life's ether",
            key = "-SKINS-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('\U0001f638 XMLer', layout)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo, skin_repo

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def get_pack(skin_repo):
    for root, dirs, files in os.walk(skin_repo):
        dirs = dirs
        for name in dirs:
            item = os.path.join(root, name)
            if "Game" in item:
                if item.split("\\")[-1] == "Game":
                    # print(item)
                    content_list.append(item)
#---------------------------------------------------------
def choose_pack(content_list):
    # ㋡
    packs = [
        [sg.Text('Choose your destiny',
                text_color='red')],
        
        [sg.InputCombo(content_list,
                default_value = "o____o",
                key = "-REPO-",
                size=(108, 31))],

        [sg.OK(key='OK'), sg.Cancel()]
    ]

    window = sg.Window("\U0001f638", packs)

    while True:
        event, values = window.read(close=True)

        copyPack = str(values["-REPO-"])

        if event == 'OK':
            print('\n\n')
            print(copyPack)
            recursive_copy(copyPack, wfpc_repo)

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def get_files(dir_src):
    pass
#---------------------------------------------------------
def recursive_copy(src, dest):
    """
    Copy each file from src dir to dest dir, including sub-directories.
    """
    for item in os.listdir(src):
        file_path = os.path.join(src, item)

        # if item is a file, copy it
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)

        # else if item is a folder, recurse 
        elif os.path.isdir(file_path):
            new_dest = os.path.join(dest, item)
            try:
                os.mkdir(new_dest)
                recursive_copy(file_path, new_dest)
            except FileExistsError:
                recursive_copy(file_path, new_dest)
#=========================================================
# DRIVE
#=========================================================
def main():
    get_pack(skin_repo)
    for i in content_list:
        print(i)
    
    choose_pack(content_list)


    source = get_pack(skin_repo)
    # get_files(source)
    # source = "d:\\_WfPC_rep\\wfpc_work\\master\\WFPC_Content_Pack_14\\14_4_WFPC_Weapon_Skins_x5_Shop\\Game"
    # recursive_copy(source, wfpc_repo)

#---------------------------------------------------------
if __name__ == "__main__":
    
    # wfpc_repo, skin_repo = Ask_Path()
    
    content_list = []
    # # ==================TEST_PATH==================================
    wfpc_repo = os.path.abspath("e:\\wfpc-minsk\\Game")
    # wfpc_repo = os.path.abspath("d:\\__some_get_come__\\__testCopy\\Game")
    skin_repo = os.path.abspath("d:\\_WfPC_rep\\wfpc_work\\master")
    # skin_repo = os.path.abspath("d:\\__some_get_come__\\__test_Weapon\\new_attachment\\Game")
    # # ==================TEST_PATH==================================

    main()