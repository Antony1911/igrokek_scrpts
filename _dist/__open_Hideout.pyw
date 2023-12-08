import time, subprocess, os
from os import name, path
import os.path
import PySimpleGUI as sg
import shutil

sg.theme('DarkGrey13')

#---------------------------------------------------------
def run_level():

    if os.path.exists("c:\\wf-skins-minsk\\Game\\Levels\\hideout_equip\\hideout_equip.cry"):
        to_level = "Game\\Levels\\hideout_equip\\hideout_equip.cry"
    else:
        sg.popup_error("Doesn't exist: \nGame\\Levels\\hideout_equip\\hideout_equip.cry")
        to_level = "Game\\Levels\\hideout_promotion\\hideout_promotion.cry"

    subprocess.Popen([Editor_path, to_level], shell = True)
#---------------------------------------------------------
def main():
    run_level()

if __name__ == "__main__":
    cry_levels = list()
    levels = dict()
    
    # ==================TEST_PATH==================================
    wfc_repo = os.path.abspath("c:\\wf-skins-minsk")
    # ==================TEST_PATH==================================
    Editor_path = wfc_repo + '\\Bin64Profile\\Editor.exe'
    path_Levels = wfc_repo + '\\Game\\Levels'

    main()