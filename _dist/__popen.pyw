import time, subprocess, os
from os import name, path
import os.path
import PySimpleGUI as sg

sg.theme('DarkGrey13')

#---------------------------------------------------------
def Ask_Path():

    layout = [
        [sg.Text('WFC repo path', text_color='yellow')],
        [sg.InputText(
            default_text = r"c:\\wf-skins-minsk",
            key = "-REPO-"),
            sg.FolderBrowse()],

        [sg.OK(key='OK'), sg.Cancel()]
    ]
    window = sg.Window('', layout)

    while True:
        event, values = window.read(close=True)

        wfc_repo = values["-REPO-"]
        # skin_repo = values["-SKINS-"]

        if event == 'OK':
            return wfc_repo

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def choose_level(cry_levels):
    # ㋡
    levels = [
        [sg.Text('Choose your destiny',
                text_color='red')],
        
        [sg.Combo(cry_levels,
                default_value = "hideout_promotion.cry",
                key = "-REPO-",
                size=(42, 31))],

        [sg.OK(key='OK'), sg.Cancel()]
    ]

    window = sg.Window('¯\_(ツ)_/¯', levels)

    while True:
        event, values = window.read(close=True)

        cry = values["-REPO-"]

        if event == 'OK':
            return cry

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
def scan_path(path_Levels):

    for root, dirs, files in os.walk(path_Levels):
        
        for i in files:
            if i.endswith('.cry'):
                cry_levels.append(i)
                levels.update({i:root})
    cry_levels.sort()
    # print([levels[cry_level] + f"\\{cry_level}"])
#---------------------------------------------------------
def run_level():
    cry_level = choose_level(cry_levels)
    
    to_level = path_Levels + '\\' + levels[cry_level].split('Levels')[1] + f'\\{cry_level}'

    subprocess.Popen([Editor_path, to_level], shell = True)
#---------------------------------------------------------
def main():
    scan_path(path_Levels)
    run_level()

if __name__ == "__main__":
    cry_levels = list()
    levels = dict()
    
    
    path = os.path.dirname(os.path.realpath(__name__)) + "\\WFPC_open.ini"
    if os.path.exists(path):
        pass
    else:
        projectPath = sg.popup_get_folder('Project path...')
        open(path, 'a').close()
        
        # не хочет записывать путь сюка
        open(path, 'a').write(projectPath)

    wfc_repo = open(path).read()
    
    # ==================TEST_PATH==================================
    # wfc_repo = os.path.abspath("e:\\partner_WPC\\wfpc_mrg\\main\\")
    # ==================TEST_PATH==================================
    Editor_path = wfc_repo + '\\Bin64Daily\\Editor.exe'
    path_Levels = wfc_repo + '\\Game\\Levels'

    main()