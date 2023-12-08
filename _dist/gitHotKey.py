import subprocess
import os.path
import os
import PySimpleGUI as sg
import git

sg.theme('DarkGrey13')


gitHotKey_path = os.path.dirname(os.path.realpath(__name__)) + "\\gitHotKey_path.ini"

if os.path.exists(gitHotKey_path):
    pass
else:
    projectPath = sg.popup_get_folder('Project path...')
    open(gitHotKey_path, 'a').close()
    open(gitHotKey_path, 'a').write(projectPath)

#---------------------------------------------------------
def Ask_Path():
    layout = [
        [sg.Button('RESET_MRG', key='-RESET_1-'), sg.Button('LOG_MRG', key='-LOG_1-')],
        [sg.Button('RESET_Work', key='-RESET_2-'), sg.Button('LOG_Work', key='-LOG_2-')],
        [sg.Button('change path_1', button_color='green', key="-CHANGE_1-")],
        [sg.Button('change path_2', button_color='green', key="--change02--")],
        [sg.CloseButton('Close', button_color="blue")]
    ]
    window = sg.Window('{}', layout, size=(200,170), grab_anywhere=1)

    while True:
        event, values = window.read()

        if event == '-RESET_1-':
            hotkey_path = open(gitHotKey_path).read()
            
            print('\n', hotkey_path + '\n' + "----"*13 + '--RESET HARD')
            gitArg01, gitArg02, gitArg03 = "git", "-C", hotkey_path
            subprocess.Popen([gitArg01, gitArg02, gitArg03, "reset", "--hard", "&&",
                                gitArg01, gitArg02, gitArg03, "clean", "-fd", "&&",
                                    gitArg01, gitArg02, gitArg03, "pull"], shell = True)
        if event == '-RESET_2-':
            work_hotkey_path = "d:\\_WfPC_rep\\wfpc_work\\"
            
            print('\n', work_hotkey_path + '\n' + "----"*13 + '--RESET HARD')
            gitArg01, gitArg02, gitArg03 = "git", "-C", work_hotkey_path
            subprocess.Popen([gitArg01, gitArg02, gitArg03, "reset", "--hard", "&&",
                                gitArg01, gitArg02, gitArg03, "clean", "-fd", "&&",
                                    gitArg01, gitArg02, gitArg03, "pull"], shell = True)

        if event == '-LOG_1-':
            hotkey_path = open(gitHotKey_path).read()
            print('\n', hotkey_path + '\n' +"----"*13 + '--LOG')
            gitArg01, gitArg02, gitArg03 = "git", "-C", hotkey_path
            subprocess.Popen([gitArg01, gitArg02, gitArg03, "log"], shell = True)
        if event == '-LOG_2-':
            work_hotkey_path = "d:\\_WfPC_rep\\wfpc_work\\"
            print('\n', work_hotkey_path + '\n' + "----"*13 + 'LOG')
            gitArg01, gitArg02, gitArg03 = "git", "-C", work_hotkey_path
            subprocess.Popen([gitArg01, gitArg02, gitArg03, "log"], shell = True)
            
        # if event == '-CHANGE_1-':
        #     # os.remove(projectPath)
        #     projectPath = sg.popup_get_folder('Project path...')
        #     open(projectPath, 'a').close()
        #     open(projectPath, 'a').write(projectPath)

        if event in ('Cancel', None) or event == sg.WIN_CLOSED:
            exit(0)
        
    window.close()
#---------------------------------------------------------
Ask_Path()