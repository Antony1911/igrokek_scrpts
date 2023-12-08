import subprocess
import os.path
import os
import PySimpleGUI as sg

sg.theme('DarkGrey13')
gif = b"d:\giphy.gif"


path = os.path.dirname(os.path.realpath(__name__)) + "\\checker_path.ini"
if os.path.exists(path):
    pass
else:
    projectPath = sg.popup_get_folder('Project path...')
    open(path, 'a').close()
    
    # не хочет записывать путь сюка
    open(path, 'a').write(projectPath)
    

checker_path = open(path).read()

arg01 = f"{checker_path}\\MRGTools"
arg02 = "\\check_backend_data.bat"
arg03 = f"{checker_path}\\Tools\\GameDataEditor\\Checker.exe"
arg04 = f"{checker_path}\\"
#---------------------------------------------------------
def Ask_Path():
    layout = [
        [sg.Button('check_backend_data', key='--backend--')],
        [sg.Button('GD_Checker', key='--gamedata--')],
        [sg.Image(data=gif0, key = 'image')],
        [sg.CloseButton('Close', button_color="blue"),
         sg.Button('change path', button_color='green', key="--change--")],
    ]
    window = sg.Window('{}', layout, size=(175,120), grab_anywhere=1)

    while True:
        event, values = window.read()
        
        if event == 'image':
            window['image'].update()

        if event == '--backend--':
            subprocess.Popen([arg01, arg02], shell = True)
        if event == '--gamedata--':
            subprocess.Popen([arg03, arg04], shell = True)
        if event == '--change--':
            os.remove(path)
            projectPath = sg.popup_get_folder('Project path...')
            open(path, 'a').close()
            open(path, 'a').write(projectPath)

        if event in ('Cancel', None, 'Exit') or event == sg.WIN_CLOSED:
            break
        
    window.close()
#---------------------------------------------------------
Ask_Path()