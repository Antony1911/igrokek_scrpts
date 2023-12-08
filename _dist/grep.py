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
hotkey_path = "e:\\partner_WPC\\wfpc_mrg\\main\\Game\\Libs\\Config\\Achievements\\"
# grep -hoe 'id="[0-9]*' *.xml | sort -nk 1.5
grep = """grep -hoe 'id="[0-9]*' *.xml | sort -nk 1.5"""

print('\n', hotkey_path + '\n' + "----"*13 + '--GREp')
subprocess.Popen(["git", "-C", hotkey_path, "grep", '-hoe', """'id="[0-9]*'""", "*.xml", "|", "sort", "-nk", "1.5"
                    ], shell = True)